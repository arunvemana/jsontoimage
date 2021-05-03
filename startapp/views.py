from django.shortcuts import render, HttpResponse
from django import forms
import json

# Create your views here.

from graphviz import Digraph


def json_to_image(data=None):
    u = Digraph('unix', format='png',
                node_attr={'color': 'lightblue2', 'style': 'filled'},
                engine='dot')
    colors = {"int": '#d25f76',
              "float": 'orange',
              "list": '#6c42c1',
              "dict": '#ae8f65',
              "str": '#96abff'}

    def get_type(var):
        return type(var).__name__

    def get_edges(treedict, parent=None, Clabel=None):
        for key in treedict.keys():
            # key_type = type(treedict[key])
            if parent:
                u.edge(parent, key, label=get_type(treedict[key]) ,fontcolor=colors[get_type(treedict[key])], color=colors[get_type(treedict[key])])
            if type(treedict[key]) not in [dict, list]:
                pass
                # u.edge(key,get_type(treedict[key]),label=get_type(treedict[key]))
            elif type(treedict[key]) is dict:
                # u.node(key)
                get_edges(treedict[key], parent=key,
                          Clabel=get_type(treedict[key]))
            elif type(treedict[key]) is list:
                # u.edge(parent,key,label="list")
                for i in treedict[key][:1]:
                    if type(i) not in [str, int, float]:
                        get_edges(i, parent=key, Clabel=get_type(i))
                    else:
                        u.edge(key, get_type(i), label=get_type(
                            i),fontcolor=colors[get_type(i)], color=colors[get_type(i)])

    if type(data) is list:
        for i, x in enumerate(data):
            if i < 1:
                get_edges(x,"List")
    elif type(data) is dict:
        main_ = "Response"
        u.node(main_)
        with u.subgraph() as s:
            s.attr(rank="same")
            for i in data.keys():
                s.node(i)
                s.edge(main_, i, label=get_type(data[i]), fontcolor=colors[get_type(data[i])],color=colors[get_type(data[i])])
        get_edges(data)
    return u.pipe()


class front_end(forms.Form):
    response = forms.JSONField()


def check(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get("response"))
            data = json_to_image(data)
        except Exception as e:
            return HttpResponse(f"Error loading the data,{e}")
        return HttpResponse(data, content_type="image/png")
    else:
        return render(request, 'index.html', {'form': front_end()})
