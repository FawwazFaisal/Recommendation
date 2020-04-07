import numpy as np
import pandas as pd
import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True

cols= ["dmc_name","complaint_type","cost: ","; garbage trucks: ","; road rollers: ","; wheel loaders: ","; cranes: ","; road graders: ","; suction trucks: ","; lorries: ","; wood chippers: ","; total distance: ","total_vehicles"]
resAlloc = pd.read_csv("ALLDMC.csv",names=cols)
def recommend(dmc_name,complaint_type,distance):
	dmc_name = float(dmc_name)
	complaint_type = float(complaint_type)
	distance = int(distance)
	result = ""
	rcmnd = resAlloc[(resAlloc["dmc_name"]==(dmc_name)) & (resAlloc["complaint_type"]== (complaint_type)) & (resAlloc["; total distance: "]==(distance*2))].sort_values(["cost: "],ascending=True).head(1).values.flatten()

	for i in range(2,(resAlloc.shape[1]-1)):
		if rcmnd[i] > 0.0:
			result+=resAlloc.columns[i] +str(int(rcmnd[i]))
	result += " KM"

	return result

@app.route('/predict', methods=['GET','POST'])
def predict():
    res = recommend(flask.request.args.get("dmc_name"),flask.request.args.get("complaint_type"),flask.request.args.get("distance"))
    return res

if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)