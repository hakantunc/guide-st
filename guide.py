import sublime, sublime_plugin
import datetime, getpass
import re

class Util():
  def getMoveValue(selfself, self, loc, edit):
    line_pos = self.view.line(loc)
    indent = selfself.getIndent(self, loc)
    line_text = self.view.substr(line_pos).strip()
    pos = line_text.find('>')
    target = line_text[:pos]
    is_increment = target.find('+')
    if (pos != -1 and is_increment != -1):
      increment_value = int(target[is_increment+1:])
      target = target[:is_increment]
      self.view.replace(edit, sublime.Region(line_pos.a + indent, line_pos.a + indent + len(target)), str(increment_value + int(target)))
    is_decrement = target.find('-')
    if (pos != -1 and is_decrement != -1):
      decrement_value = int(target[is_decrement+1:])
      target = target[:is_decrement]
      if (-decrement_value + int(target) > 0 ):
        self.view.replace(edit, sublime.Region(line_pos.a + indent, line_pos.a + indent + len(target)), str(-decrement_value + int(target)))
    m = re.search('^\d+$',target)
    if m:
      times = int(m.group(0))
    else:
      times = 999
    return times
  def getIndent(selfself, self, loc):
    line = self.view.substr(self.view.line(loc))
    if (len(line) == 0):
      return -1
    m = re.search('(^[ ]*)[^ ]',line)
    indent = len(m.group(1))
    return indent

class MoveBlockCommand(sublime_plugin.TextCommand):
  def run(self, edit, is_add_date = False):
    if is_add_date:
      self.view.run_command('add_date_time')
    loc = self.view.sel()[0]
    move_value = Util().getMoveValue(self, loc, edit)
    line_pos = self.view.line(loc)
    beg = line_pos.a
    end = line_pos.b
    line_text = self.view.substr(line_pos)
    m = re.search('(^[ ]*)[^ ]',line_text)
    base_ind = len(m.group(1))
    next_ind = base_ind + 1
    while (next_ind>base_ind):
      end = line_pos.b
      next_line_pos = self.view.line(line_pos.b+1)
      if (len(next_line_pos) == 0 ):
        break
      next_line = self.view.substr(next_line_pos)
      m = re.search('(^[ ]*)[^ ]',next_line)
      next_ind = len(m.group(1))
      line_pos = next_line_pos

    r = sublime.Region(beg, end)
    self.view.sel().add(r)
    for _ in range(move_value):
      next_line_indent = Util().getIndent(self, self.view.sel()[0].b+1)
      if (next_line_indent < base_ind):
        break
      if (next_line_indent == base_ind):
        self.view.run_command('swap_line_down')
        next_line_indent = Util().getIndent(self, self.view.sel()[0].b+1)
        while (next_line_indent > base_ind):
          self.view.run_command('swap_line_down')
          next_line_indent = Util().getIndent(self, self.view.sel()[0].b+1)
      else:
        self.view.run_command('swap_line_down')

    self.view.sel().clear()
    # self.view.run_command('fold_by_level', {"level": 1})
    # self.view.sel().add(beg)
    # self.view.show(beg)
    # self.view.run_command('unfold')
    # self.view.sel().clear()
    self.view.sel().add(beg)
    self.view.show(beg)

class LoggingCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    pass
    # daily output
    # weekly output
    # monthly output
    # yearly output
    # last 7 days
    # last 30 days
    # 1 get the logs of line and put them into a list
    log_list = ''
    # 2 

class CalculatePercentageCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    print_length = 100
    print('beg#percentage')

    # 1 Read data into a data structure

    size = self.view.size()
    init_loc = self.view.line(self.view.sel()[0]).a
    lines = self.view.lines(sublime.Region(init_loc,size))

    list = []

    increment = '0'
    for line in lines:
      text = self.view.substr(line)
      if len(text) <= 0:
        continue
      if text[0] == ' ':
        continue
      if (text == '###'):
        break
      pos_lt = text.find('>')
      pos_pipe = text.find('|')
      if (pos_pipe == -1):
        pos_pipe = len(text)

      if (pos_lt != -1):
        value = text[:pos_lt].strip()
        task = text[pos_lt+1:pos_pipe].strip().strip('>')

        increment = '0'
        pos_plus = value.find('+');
        pos_minu = value.find('-');
        if (pos_plus != -1):
          increment = value[pos_plus:]
          value = value[:pos_plus]
        elif (pos_minu != -1):
          increment = value[pos_minu:]
          value = value[:pos_minu]
        m = re.search('^\d+$',value)
        if m:
          value = int(m.group(0))
        else:
          value = 999
      else:
        value = 999
      list.append( { 'value': value, 'task': text, 'played': 0, 'increment': int(increment) } )

    if (len(list) == 0 ):
      print('Guide: no item')
      return

    # 2 Simulate the data and populate the usage
    simulation_number = 9999
    for i in range(simulation_number):
      # print(i)
      list[0]['played'] = list[0]['played'] + 1
      if 'first' not in list[0]:
        list[0]['first'] = i
      pos = 0
      val = list[0]['value']
      # list[0]['value'] += list[0]['increment']
      # list[0]['value'] = max(list[0]['value'], 1)
      for _ in range(int(val)):
        if (pos+1 == len(list)):
          break
        list[pos], list[pos+1] = list[pos+1], list[pos]
        pos = pos + 1

    for element in list:
      if 'first' not in element:
        element['first'] = simulation_number

    # 3 Output the results

    list = sorted(list, key=lambda val: val['first'], reverse = False)
    self.f(list, simulation_number, print_length)

    print('###\n###')

    list = sorted(list, key=lambda val: val['played'], reverse = True)
    self.f(list, simulation_number, print_length)

    head_tail_n = 5
    print('###\n--First and last few tasks###')
    list = sorted(list, key=lambda val: val['first'], reverse = False)
    self.f(list[:head_tail_n], simulation_number, print_length)
    print('---')
    self.f(list[-head_tail_n:], simulation_number, print_length)
    print('number of tasks: ' + str(len(list)))

  def f(self, list, simulation_number, print_length):
    for element in list:
      percentage = round(100 * element['played']/simulation_number, 1)
      first = str(element['first'])
      val = str(element['value'])
      if (val == '999'):
        val = '>'
      print(str(percentage) + '%\t\t' + str(percentage*70/100) + ' ' +
        val + '>(' + first + ')' + element['task'][:print_length])


class MoveToLaterCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command("move_task_batch", {'times': 99 })

class SetupHomeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    pos = self.view.find('\d+>@research', 0)
    self.view.replace(edit,pos,'5>@research')
    self.view.run_command('go_to_first_line')

class SetupWorkCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    pos = self.view.find('\d+>@research', 0)
    self.view.replace(edit,pos,'1>@research')
    line_pos = self.view.line(pos)
    line_text = self.view.substr(line_pos)
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(line_pos.a))
    self.view.show(line_pos.a)
    for _ in range(99):
      self.view.run_command('swap_line_up')
    self.view.run_command('swap_line_down')
    self.view.run_command('go_to_first_line')

# end>[work:]work; another work; | 11/12:37/4/14 | 9/17:16/4/14
class ParseLineCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print('beg')
    loc = self.view.sel()[0]
    line_pos = self.view.line(loc)
    line_text = self.view.substr(line_pos)#.strip()
    print(line_text)
    return line_text

class HorizontalTaskCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # line = self.view.window().run_command('parse_line')
    # print(line)
    pass
    h = HorizontalTask()
    h.pp()

class MoveTaskCommand(sublime_plugin.TextCommand):
  def run(self, edit, is_add_date = False):
    loc = self.view.sel()[0]
    line_pos = self.view.line(loc)
    line_text = self.view.substr(line_pos).strip()

    pos = line_text.find('>')
    target = line_text[:pos]
    m = re.search('^\d+$',target)
    if m:
      times = int(m.group(0))
    elif (target == 'end'):
      times = 99
    elif (target == '~'):
      self.view.window().run_command('prompt_move_task')
      return
    else:
      times = 99

    self.view.run_command("move_task_batch", {'times': times, 'is_add_date': is_add_date, 'stop_before': True })

class PromptMoveTaskCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel('Move Down', '', self.on_done, None, None)
    pass
  def on_done(self, value):
    self.window.run_command('move_task_batch', { 'times': int(value), 'is_add_date': True } )

class GoToFirstLine(sublime_plugin.TextCommand):
  def run(self, edit, pos = 0):
    # pos = 0
    # if (position_region != 0):
    #   line = self.view.line(position_region)
    #   pos = line.a
    self.view.sel().clear()
    self.view.sel().add(sublime.Region(pos))
    self.view.show(pos)

class MoveTaskBatchCommand(sublime_plugin.TextCommand):
  def run(self, edit, times, is_add_date = False, stop_before = False):
    init_loc = self.view.line(self.view.sel()[0]).a
    for _ in range(times):
      if (stop_before):
        loc = self.view.sel()[0]
        line_pos = self.view.line(loc)
        next_line_pos = self.view.line(line_pos.b+1)
        next_line_text = self.view.substr(next_line_pos)
        if (next_line_text == '###'):
          break
      self.view.run_command('swap_line_down')
    if ( is_add_date == True):# and times > 0):
      self.view.run_command('add_date_time')
    self.view.run_command('go_to_first_line', { 'pos': init_loc })#, { 'position_region': init_loc })

# http://stackoverflow.com/a/13882791
class AddDateTimeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    loc = self.view.sel()[0]
    line_pos = self.view.line(loc)
    line_text = self.view.substr(line_pos)
    pos = line_text.find('|')
    text = datetime.datetime.now().strftime("| %-d/%H:%M/%-m/%y ")
    if (pos==-1):
      pos = len(line_text)
      text = " " + text.strip()
    self.view.insert(edit, line_pos.a + pos, text)
