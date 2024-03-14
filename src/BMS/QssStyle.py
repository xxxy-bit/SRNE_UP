RED_ProgressBar = """
    QProgressBar{
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #F26659
    }
"""
        
GREEN_ProgressBar = """
    QProgressBar{
        text-align: center;
    }

    QProgressBar::chunk {
        background-color:#57C788;
    }
"""
test_ProgressBar = """
    QProgressBar{
        text-align: center;
    }

    QProgressBar::chunk {
        # background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #C2FCD4,stop:1 #0DCDA4);
    }
"""
batl_LineEdit = """
    QLineEdit{
        border: 0px;
    }
"""

cellTmp_LineEdit = """
    QLineEdit{
        border: 0px;
        background-color: #E5F2FC
    }
"""

cellTmp2_LineEdit = """
    QLineEdit{
        border: 0px;
        background-color: #F7F7F7
    }
"""

cellVol1_LineEdit = """
    QLineEdit{
        border: 0px;
        font: 20px
    }
"""

cellVol2_LineEdit = """
    QLineEdit{
        border: 0px;
        background-color: #FCF2EB
    }
"""

close_Button = """
    QPushButton{
        border: 1px solid #F88D20;
        background-color: #FFFFFF;
        color: #F88D20
    }
"""

open_Button = """
    QPushButton{
        border: 1px solid #F88D20;
        background-color: #F88D20;
        color: #FFFFFF
    }
    
    QPushButton:hover{
        background: #fc7e00;
    }

    QPushButton:pressed{
        color: #F88D20;
        background: rgba(249, 249, 249, 0.3);
    }
"""

bin_cell_LineEdit = """
    QLineEdit{
        border: 0px;
        background-color: #FCEEE5;
    }
"""

bin_cell2_LineEdit = """
    QLineEdit{
        border: 0px;
        background-color: #E5F2FC;
    }
"""

sys_label = """
    QLabel{
        font-size: 10pt;
        color: #626262;
    }
"""

sys_Line = """
    QLineEdit{
        background-color:#FFFFFF;
        font-size: 18pt;
        border: 1px solid #dcd8d8;
    }
"""

table_bg = """
    QWidget{
        background-color: #FBF9F8
    }
"""

white_bg = """
    QWidget{
        background-color: #ffffff;
    }
    QGroupBox {
        border: 0px;
        padding: 10px 5px 5px 5px;
        border-radius: 5px
    }
    QTableWidget {
        border: 0px;
    }
"""