
"""
This script contains basic stylings for all windows
"""

main_stylesheet = """
    QLabel {
      qproperty-alignment: AlignCenter;
    }
    

    QFrame#church {
      background-color: rgba(4, 18, 41, 0.7);
      border-radius: 5px;
    }

    QFrame#train {
      background-color: rgba(4, 18, 41, 0.7);
      border-radius: 5px;
    }

    QFrame#playground {
      background-color: rgba(4, 18, 41, 0.7);
      border-radius: 5px;
      opacity: 0.5;
    }
    
    QFrame#church:hover {
      background-color: #041229;
    }

    QFrame#train:hover {
      background-color: #041229;
    }

    QFrame#playground:hover {
      background-color: #041229;
    }


    QFrame#frame_2 {
      background-color: #041229;
    }


    QLabel#church_lb {
      font: 25px;
    }

    QLabel#train_lb {
      font: 25px;
    }

    QLabel#label {
      color: white;
    }

    QLabel#label_2 {
      color: white;
    }

    QLabel#playground_lb {
      font: 25px;
    }

    QLabel#header {
      background-color: #041229;
      color: white;
      font: 50px;
      qproperty-alignment: AlignCenter;
    }

     QMainWindow#MenuWindow{
      border-image:url(/home/christopher/NSO_LIFE/Practice/byu.jpg) 0 0 0 0 stretch stretch;
      }
    
      QMainWindow#AIWindow{
      border-image:url(/home/christopher/NSO_LIFE/Practice/byu.jpg) 0 0 0 0 stretch stretch;
      }

   QMainWindow#MainWindow{
        border-image:url(/home/christopher/NSO_LIFE/Practice/eb.png) 0 0 0 0 stretch stretch;
       }

    QFormLayout#formLayoutWidget {
      font: 50px;
    }

    """