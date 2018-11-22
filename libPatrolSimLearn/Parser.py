import xml.etree.ElementTree as ET
import copy
from Agent import *

def ReadXML(fileName, mapSizeX, mapSizeY, sizeOfGrid):
    doc = ET.parse(fileName)
    root = doc.getroot()
    agentList = list()

    for _agentList in root:
        if(_agentList.tag == "AgentList"):
            for _agent in _agentList: # Agent
                # agnet_name = _agent.attrib["name"]
                id, sc = _agent.attrib["id"].split('_')
                agent_id = int(id)
                agnet_sc = int(sc)
                agent_spd = float(_agent.attrib["spd"])
                agent_type = int(_agent.attrib["type"])
                agent = Agent(agent_id, agnet_sc, "None", agent_type, agent_spd, mapSizeX, mapSizeY, sizeOfGrid)

                waypoints = _agent.find('Waypoints')
                #print(agent_id, agent_spd, agent_type, waypoints)
                for _point in waypoints:
                    x = float(_point.attrib["x"])
                    y = float(_point.attrib["y"])
                    z = float(_point.attrib["z"])
                    if x > 100:
                        x = 100
                    if y > 100:
                        y = 100
                    if z > 100:
                        z = 100
                    #y = 100 - y
                    point = Point(x, y, z)
                    agent.addWayPoint(point)
                agentList.append(agent)
        return agentList
