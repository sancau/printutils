import printutils  # import the module

# it's possible to change printutils behavior, though you shouldn't
# if config will be not passed it will just fall back to defaults
config = printutils.Config()
config.timestamp = True  # timestamp on / off
config.timestamp_format = '%H-%M'  # specify a timestamp format
config.title = True  # title on / off
config.allow_print = True  # you can even restrict prints at all (ex: in prod.)
config.decorate_pure_print = True  # add PrintUtils behavior to pure prints too

# initialize it and pass identifier and config:
printutils.init(config=config)

# now just use it like that
# the rule of thumb here is that the code will behave just like
# you would expect it to behave, basically similar to the original print()
print('pure', 'python', 'print', 42, '\n')
print.log('log', 42, '\n')
print.error('error', 42, '\n')
print.success('success', 42, '\n')
print.warning('warning', 42, '\n')
print.info('info', 42, '\n')

# if you're against shadowing builtin print() - pass kwarg explicit=True
# so the PrintUtils instance will be returned explicitly and there will be
# no modifications to the calling module __dict__
# You can assign the PrintUtils instance to any variable and use it like that
console = printutils.init(explicit=True, config=config)
console.success('Explicit PrintUtils call', 42)  # all the magic
