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

all_btn = """
    PushButton{
        color: black;
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(0, 0, 0, 0.073);
        border-bottom: 1px solid rgba(0, 0, 0, 0.183);
        border-radius: 5px;
        /* font: 14px 'Segoe UI', 'Microsoft YaHei'; */
        padding: 5px 12px 6px 12px;
        outline: none;
    }
"""