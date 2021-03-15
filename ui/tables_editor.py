
import sys
import os
from .xml_editor import addUi
from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtSql, uic

ui_path = os.path.dirname(os.path.abspath(__file__))
modify_table_dialogUi= uic.loadUiType(os.path.join(ui_path, "modify_table_dialog.ui"))[0]
TYPE_DICT={1:"BOOLEAN", 2:"INTEGER",6:"NUMERIC", 10:"TEXT", 12:"BLOB"}


class ModifyTableDialog(QtWidgets.QDialog, modify_table_dialogUi):
    def __init__(self, parent=None, *args):
        super(ModifyTableDialog, self).__init__(*args)
        self.parent=parent
        self.setupUi(self)
        self.model=self.tableWidget.model()
        self.buttonBox.buttons()[0].setEnabled(False)
        self.commandLinkButton_2.setEnabled(False)
        self.rc_count=0
        self.ai_button_group=QtWidgets.QButtonGroup()

    def update_code_text(self):
        data = []
        pk_fields=[]
        pk_auto=False
        for row in range(self.model.rowCount()):
            auto_incr= ''
            field_name = self.tableWidget.item(row,0).text()
            field_type=''
            field_not=''
            if self.tableWidget.cellWidget(row,1):
                field_type = self.tableWidget.cellWidget(row,1).currentText()
            if self.tableWidget.cellWidget(row,4):

                field_not_item = self.tableWidget.cellWidget(row,2)
                
                if self.tableWidget.cellWidget(row,2).isChecked(): field_not = ' NOT NULL'
                

                if self.tableWidget.cellWidget(row,3).isChecked(): pk_fields.append(field_name)
            
                if self.tableWidget.cellWidget(row,4).isChecked(): 
                    auto_incr = ' PRIMARY KEY AUTOINCREMENT'
                    pk_auto=True
                     
            data.append((field_name,field_type, field_not, auto_incr))
                    
        if pk_auto : pk_fields=[]       
           
                
        sql_lines=[]
        for r in data:
            sql_lines.append( '    `%s`  `%s`  %s  %s' % (r[0], r[1], r[2], r[3])) 
    
        if pk_fields: sql_lines.append('    PRIMARY KEY('+','.join(pk_fields)+')')
        
        
        self.query='CREATE TABLE `%s` (\n' % self.lineEdit.text()

        

        self.query +=',\n'.join(sql_lines)
        
        self.query +='\n)'
    
        self.textEdit.setText(self.query)
        
        if self.lineEdit.text() and sql_lines: 
            self.buttonBox.buttons()[0].setEnabled(True)
            addUi(self.lineEdit.text(),newForm=True)        #adding new form for each table
            addUi(self.lineEdit.text(),newForm=False,newField=True)        #adding new form for each table
        
        else: self.buttonBox.buttons()[0].setEnabled(False)
       
        
    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self):

        self.update_code_text()


    @QtCore.pyqtSlot('QTableWidgetItem*')
    def on_tableWidget_itemClicked(self, item):
        pass
    @QtCore.pyqtSlot(int, int)
    def on_tableWidget_cellClicked(self, r, c):
        pass

    @QtCore.pyqtSlot()
    def on_tableWidget_itemSelectionChanged(self):
        self.commandLinkButton_2.setEnabled(True)


    @QtCore.pyqtSlot('QTableWidgetItem*')
    def on_tableWidget_itemChanged(self, item):
        self.update_code_text()

    @QtCore.pyqtSlot()
    def on_commandLinkButton_2_clicked(self):
        sm=self.tableWidget.selectionModel()
        r=sm.selectedRows()[0].row()
        self.tableWidget.removeRow(r)
        self.tableWidget.update()
        self.update_code_text()
        
    @QtCore.pyqtSlot()
    def on_commandLinkButton_clicked(self):
        
        rc=self.tableWidget.rowCount()
        self.tableWidget.insertRow(rc)
        self.tableWidget.setItem(rc, 0, QtWidgets.QTableWidgetItem("Field%d" % self.rc_count))
        self.rc_count+=1
        type_combo = QtWidgets.QComboBox()
        for t in TYPE_DICT.values():
                type_combo.addItem(t)
        self.tableWidget.setCellWidget(rc, 1, type_combo)
        type_combo.currentIndexChanged.connect(self.update_code_text)

        if rc==0: type_combo.setCurrentIndex(1)
        else: type_combo.setCurrentIndex(3)
   
        not_check_box=QtWidgets.QCheckBox()
        self.tableWidget.setCellWidget(rc, 2, not_check_box)
        not_check_box.clicked.connect(self.update_code_text)
        
        pk_check_box=QtWidgets.QCheckBox()
        self.tableWidget.setCellWidget(rc, 3, pk_check_box)
        pk_check_box.clicked.connect(self.clear_primary_key)

        ai_check_box=QtWidgets.QCheckBox()
        self.tableWidget.setCellWidget(rc, 4, ai_check_box)
        self.ai_button_group.addButton(ai_check_box)
        ai_check_box.clicked.connect(self.make_primary_key)
        
    def make_primary_key(self):
        for row in range(self.model.rowCount()):
            ai=self.tableWidget.cellWidget(row,4)
            if ai:
                pk=self.tableWidget.cellWidget(row,3)
                if ai.isChecked():
                    pk.setChecked(True)
                    type_combo=self.tableWidget.cellWidget(row,1)
                    type_combo.setCurrentIndex(1)
                    
                else:
                    pk.setChecked(False)
  
        self.update_code_text()
    
    def clear_primary_key(self):
        self.ai_button_group.setExclusive(False)
        for row in range(self.model.rowCount()):
            ai=self.tableWidget.cellWidget(row,4)
            ai.setChecked(False)
        self.ai_button_group.setExclusive(True)
        self.update_code_text() 

        
    @QtCore.pyqtSlot()
    def on_buttonBox_accepted(self):
        
        if not self.parent.execute_query(self.query):
            self.parent.update_tables_table()
            self.close()


    @QtCore.pyqtSlot()
    def on_buttonBox_rejected(self):
        self.close()


