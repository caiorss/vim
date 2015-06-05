
import vim
import re

def uncurry(func):
    return lambda atuple:  func(*atuple)

def juxt(funcs):
    return lambda x: tuple(map(lambda f: f(x), funcs))

def attr(name):
    return lambda obj: getattr(obj, name)

def list_buffers():
    return map(juxt([attr("number"), attr("name")]), vim.buffers)

def foreach(f, xs):
    for x in xs:
        f(x)

def show_buffers():
    format_line = lambda name, number: " {} {}".format(name, number)
    lines = map(uncurry(format_line), list_buffers())
    print(str.join("\n", lines))


def read_buffer(buf):
    return str.join("\n", buf[:])

def read_buffer_lines(buf):
    return buf[:]

def read_current_buffer():
    return read_buffer(vim.current.buffer)

def lines_current_buffer():
    return read_buffer_lines(vim.current.buffer)

def clear_current_buffer():
    del vim.current.buffer[:]

def find_todo():
    lines = lines_current_buffer()
    f = filter(lambda t: re.match("@TODO:\s*.*", t[1]), enumerate(lines, start=1))
    print(f)

def close_buffer(buf):
    cmd = "bw! " + buf.name 
    vim.command(cmd)

def close_empty_buffers():

    bufs = map(lambda i: vim.buffers[i[0]] ,filter(lambda t: t[1] == "",
        list_buffers()))
    
    foreach(close_buffer, bufs) 
 
def replace(pattern, val):
    txt = read_current_buffer()
    newtxt = re.sub(pattern, val, txt)
    clear_current_buffer()
    foreach(vim.current.buffer.append, newtxt.splitlines())
 
def loadbuffer():
    code = read_current_buffer()
    exec(code, globals())
