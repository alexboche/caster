
import imp
import sys
import types
import weakref

from caster.lib import settings


func_attrs = ['__code__', '__defaults__', '__doc__',
              '__closure__', '__globals__', '__dict__']


def update_function(old, new):
    """Upgrade the code object of a function"""
    for name in func_attrs:
        try:
            setattr(old, name, getattr(new, name))
        except (AttributeError, TypeError):
            pass


def update_class(old, new):
    """Replace stuff in the __dict__ of a class, and upgrade
    method code objects, and add new methods, if any"""
    for key in list(old.__dict__.keys()):
        old_obj = getattr(old, key)
        try:
            new_obj = getattr(new, key)
            if old_obj == new_obj:
                continue
        except AttributeError:
            # obsolete attribute: remove it
            try:
                delattr(old, key)
            except (AttributeError, TypeError):
                pass
            continue

        if update_generic(old_obj, new_obj): continue

        try:
            setattr(old, key, getattr(new, key))
        except (AttributeError, TypeError):
            pass # skip non-writable attributes

    for key in list(new.__dict__.keys()):
        if key not in list(old.__dict__.keys()):
            try:
                setattr(old, key, getattr(new, key))
            except (AttributeError, TypeError):
                pass # skip non-writable attributes


def update_property(old, new):
    """Replace get/set/del functions of a property"""
    update_generic(old.fdel, new.fdel)
    update_generic(old.fget, new.fget)
    update_generic(old.fset, new.fset)


def isinstance2(a, b, typ):
    return isinstance(a, typ) and isinstance(b, typ)


UPDATE_RULES = [
    (lambda a, b: isinstance2(a, b, type),
     update_class),
    (lambda a, b: isinstance2(a, b, types.FunctionType),
     update_function),
    (lambda a, b: isinstance2(a, b, property),
     update_property),
]
UPDATE_RULES.extend([(lambda a, b: isinstance2(a, b, types.MethodType),
                      lambda a, b: update_function(a.__func__, b.__func__)),
])


def update_generic(a, b):
    for type_check, update in UPDATE_RULES:
        if type_check(a, b):
            update(a, b)
            return True
    return False


class StrongRef(object):
    def __init__(self, obj):
        self.obj = obj
    def __call__(self):
        return self.obj


def superreload(module, reload=reload, old_objects=None):
    """Enhanced version of the builtin reload function.
    superreload remembers objects previously in the module, and
    - upgrades the class dictionary of every old class in the module
    - upgrades the code object of every old function and method
    - clears the module's namespace before reloading
    """
    if old_objects is None:
        old_objects = {}

    # collect old objects in the module
    for name, obj in list(module.__dict__.items()):
        if not hasattr(obj, '__module__') or obj.__module__ != module.__name__:
            continue
        key = (module.__name__, name)
        try:
            old_objects.setdefault(key, []).append(weakref.ref(obj))
        except TypeError:
            pass

    # reload module
    try:
        # clear namespace first from old cruft
        old_dict = module.__dict__.copy()
        old_name = module.__name__
        module.__dict__.clear()
        module.__dict__['__name__'] = old_name
        module.__dict__['__loader__'] = old_dict['__loader__']
    except (TypeError, AttributeError, KeyError):
        pass

    try:
        module = reload(module)
    except:
        # restore module dictionary on failed reload
        module.__dict__.update(old_dict)
        raise

    # iterate over all objects and update functions & classes
    for name, new_obj in list(module.__dict__.items()):
        key = (module.__name__, name)
        if key not in old_objects: continue

        new_refs = []
        for old_ref in old_objects[key]:
            old_obj = old_ref()
            if old_obj is None: continue
            new_refs.append(old_ref)
            update_generic(old_obj, new_obj)

        if new_refs:
            old_objects[key] = new_refs
        else:
            del old_objects[key]

    return module




def reload_grammar(module_path, *args, **kwargs):
    print('reload grammar', module_path, args, kwargs)
    cached_module = sys.modules[module_path]    
    cached_module.grammar.unload()
    superreload(cached_module, reload=imp.reload)
    cached_module.grammar.load()


def reload_app_grammars(*args, **kwargs):
    print('reload all app grammars', args, kwargs)
    for path in settings.MODULES_TO_RELOAD:
            reload_grammar(path)    
    return ''