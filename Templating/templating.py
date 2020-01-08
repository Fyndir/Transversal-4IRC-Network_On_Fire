from jinja2 import Template, Environment, FileSystemLoader
import yaml
import sys

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("jinja.j2")

with open("data.yaml", 'r') as datafile:
	context = yaml.load(datafile)

output = template.render(**context)
print(output)

f = open('config.conf','w')
f.write(output)
f.close