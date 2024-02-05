from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import pandas as pd

with open ("model.pickle","rb") as f:
        mp = pickle.load(f)

def predict(l, model):
    dataset = pd.DataFrame({"data1" : [l[0]],
                        "data2" : [l[1]],
                        "data3" : [l[2]],
                        "data4" : [l[3]],
                        "data5" : [l[4]],
                        "data6" : [l[5]]})
    
    return model.predict(dataset)



app = Flask(__name__)
app.secret_key = "234@#3334@#$@#$23#@$@#$@%^&%^&45$#%#$%#$%"


@app.route("/")
def home(reset = True):
    if reset:
        session["li"] = [0 for _ in range(7)]
        session["correct"] = 1
        session["wrong"] = 0
        session["total"] = 1
        session["graph_data"] = [[0,0]]
    session["percentage"] = round((session["correct"]/session["total"])*100, 3)
    return render_template("index.html",graph_data = session["graph_data"], correct = session["correct"]-1,
                           wrong = session["wrong"], total = session["total"]-1,
                           percentage = session["percentage"])

@app.route("/left")
def left():
    session["li"].pop(0)
    session["li"].append(0)
    pre = predict(session["li"],mp)
    if pre == 0:
        session["correct"] += 1
        new_coor = [session["graph_data"][-1][0]+1,session["graph_data"][-1][0]+1]
        session["graph_data"].append(new_coor)
    else:
        session["wrong"] += 1
        new_coor = [session["graph_data"][-1][0]+1,session["graph_data"][-1][0]-1]
        session["graph_data"].append(new_coor)
    
    session["total"] += 1

    return home(reset = False)

@app.route("/right")
def right():
    session["li"].pop(0)
    session["li"].append(1)
    pre = predict(session["li"],mp)
    if pre == 1:
        session["correct"] += 1
        new_coor = [session["graph_data"][-1][0]+1,session["graph_data"][-1][0]+1]
        session["graph_data"].append(new_coor)
    else:
        session["wrong"] += 1
        new_coor = [session["graph_data"][-1][0]+1,session["graph_data"][-1][0]-1]
        session["graph_data"].append(new_coor)
    
    session["total"] += 1

    return home(reset = False)

if __name__ == "__main__":
    app.run(debug=True)