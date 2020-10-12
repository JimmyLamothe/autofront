def print_name(name = None):
    if not name:
        name = __name__
    print('__name__ == {}'.format(name))

def print_name_sys():
    import sys
    frame = sys._getframe().f_back
    frame_info = traceback.extract_stack(f=frame, limit=1)[0]
    name = getattr(frame_info, 'name', frame_info[2])
    return name
    
if __name__ == '__main__':
    print_name()
