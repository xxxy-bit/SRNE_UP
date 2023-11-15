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