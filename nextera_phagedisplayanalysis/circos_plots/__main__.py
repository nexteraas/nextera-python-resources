import matplotlib.pyplot as plt
import numpy as np

import svgutils.compose as sc


# sc.Figure("750px", "800px",
#         sc.Text("Alkhoiuhasadasdasd", '0px', '25px', size='25px'),
#         sc.SVG("C:/docker_data_exchange/out/tableview.svg").scale(0.25).move(0, 50),
#           sc.Grid(100, 100)
#         ).save("C:/docker_data_exchange/out/tableview_compose.svg")

sc.Figure("750px", "1550px",
          sc.Panel(
        sc.Text("R0",'1px', '25px', size='25px'),
        sc.SVG("C:/docker_data_exchange/out/tableview.svg").scale(0.25).move(0, 50)
    ),
sc.Panel(
        sc.Text("R1",'1px', '25px', size='25px'),
        sc.SVG("C:/docker_data_exchange/out/tableview2.svg").scale(0.25).move(0, 50)
    )
          ).tile(1,2).save("C:/docker_data_exchange/out/compose.svg")