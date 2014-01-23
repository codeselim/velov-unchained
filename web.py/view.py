#This file prepares the view variables
import web
import model
import config

t_globals = dict(
  datestr=web.datestr, 
)
render = web.template.render('templates/', cache=config.cache, globals=t_globals)
render._keywords['globals']['render'] = render

def listing(**k):
    l = model.listing(**k)
    return render.listing(l)
