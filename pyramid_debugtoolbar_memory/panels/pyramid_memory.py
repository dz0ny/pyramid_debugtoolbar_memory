# -*- coding: utf-8 -*-
"""Memory Debug toolbar."""
from pympler import asizeof
from pympler.classtracker import ClassTracker
from pympler.process import ProcessMemoryInfo
from pympler.util.stringutils import pp
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_debugtoolbar.panels import DebugPanel

_ = lambda x: x


def process_history(h):
    r = []
    for i in h:
        r.append(str(i))
    return ','.join(r)


def get_memory_object(req):
    initial_size = asizeof.basicsize(req) or 0
    return asizeof.Asized(initial_size, initial_size)


class MemoryDebugPanel(DebugPanel):
    """
    Sample debug panel
    """
    name = 'memory'
    has_content = True
    template = 'pyramid_debugtoolbar_memory.panels:templates/memory.dbtmako'
    title = _('Memory')
    nav_title = title

    def __init__(self, request):
        self._tracker = ClassTracker()
        self._tracker.track_class(Request)
        self._tracker.track_class(Response)

    def wrap_handler(self, handler):
        handler = self._wrap_profile_handler(handler)
        return handler

    def _wrap_profile_handler(self, handler):
        def profiler_handler(req):
            self._tracker.create_snapshot('before')
            before = ProcessMemoryInfo()
            req_before = get_memory_object(req.registry)
            try:
                result = handler(req)
            except:
                raise
            finally:
                after = ProcessMemoryInfo()
                self._tracker.create_snapshot('after')
                class_stats = self._tracker.stats
                class_stats.annotate()
                self.stats = dict(
                    before=before,
                    after=after,
                    class_stats=class_stats,
                    req_before=req_before,
                    req_after=get_memory_object(req.registry),
                )
            return result

        return profiler_handler

    def render_vars(self, req):
        before = self.stats['before']
        after = self.stats['after']
        class_stats = self.stats['class_stats']
        rows = [('Resident set size', after.rss),
                ('Virtual size', after.vsz),
                ]

        rows.extend(after - before)
        rows = [(key, pp(value)) for key, value in rows]
        rows.extend(after.os_specific)
        classes = []
        snapshot = class_stats.snapshots[-1]
        for model in class_stats.tracked_classes:
            history = [cnt for _, cnt in class_stats.history[model]]
            size = snapshot.classes.get(model, {}).get('sum', 0)
            if history and history[-1] > 0:
                classes.append((model, history, pp(size)))
        return {
            'rows': rows,
            'classes': classes,
            'process_history': process_history,
            'req_before': self.stats['req_before'],
            'req_after': self.stats['req_after'],
        }
