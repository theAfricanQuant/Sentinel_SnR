"""
Created on Tues October 7 2020 18:55
@author: Beven Nyamande
"""

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sentinel import plot_support_n_resistance

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
	""" Display the userfriendly home page """

	return templates.TemplateResponse('index.html', {"request": request, 
		                                             "path": None})


@app.post('/')
async def get_params_and_plot_chart(request: Request, pair: str = Form('pair'),
	                                tf: str = Form('tf')):
	""" Calculate and plot the chart.
	    Return the chart to the web application
	    variables
	        pair: str
	        tf: str
	"""
	path = plot_support_n_resistance(pair, tf)
	return templates.TemplateResponse('index.html', {"request": request, "path": path})



if __name__ == '__main__':
	uvicorn.run(app, debug=True)


