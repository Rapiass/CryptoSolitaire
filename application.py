from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
import sys
import pyperclip
from jeudecartes import JeuDeCartes
from cryptage import coder, decoder


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptage Solitaire")
        self.setStyleFromFile("style.qss")
        self.paquet_copie = None
        self.setup_ui()

    def setStyleFromFile(self, filename):
        with open(filename, "r") as f:
            self.setStyleSheet(f.read())

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Fichier à crypter 
        self.btn_select_file = QPushButton("📂 Sélectionner un fichier .txt")
        self.btn_select_file.clicked.connect(self.load_txt_file)
        layout.addWidget(self.btn_select_file)

        self.btn_encrypt_file = QPushButton("🔐 Crypter et exporter")
        self.btn_encrypt_file.clicked.connect(self.encrypt_file)
        layout.addWidget(self.btn_encrypt_file)

        # Fichier à décrypter 
        self.btn_select_crypt_file = QPushButton("📂 Sélectionner un fichier .crypt")
        self.btn_select_crypt_file.clicked.connect(self.load_crypt_file)
        layout.addWidget(self.btn_select_crypt_file)

        self.paquet_path_button = QPushButton("Sélectionner le fichier .paquet")
        self.paquet_path_button.clicked.connect(self.select_paquet_file)
        layout.addWidget(self.paquet_path_button)

        self.paquet_label = QLabel("Aucun fichier .paquet sélectionné")
        layout.addWidget(self.paquet_label)

        self.btn_decrypt_file = QPushButton("🔓 Décrypter le fichier")
        self.btn_decrypt_file.clicked.connect(self.decrypt_file)
        layout.addWidget(self.btn_decrypt_file)

        # Saisie manuelle d’un message 
        layout.addWidget(QLabel("Message à coder :"))
        self.message_input = QLineEdit()
        layout.addWidget(self.message_input)

        # Type de paquet
        layout.addWidget(QLabel("Type de paquet :"))
        self.radio_group = QButtonGroup(self)
        self.radio_classique = QRadioButton("Classique")
        self.radio_aleatoire = QRadioButton("Aléatoire")
        self.radio_personnalise = QRadioButton("Personnalisé")
        self.radio_aleatoire.setChecked(True)

        for btn in [self.radio_classique, self.radio_aleatoire, self.radio_personnalise]:
            self.radio_group.addButton(btn)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_classique)
        radio_layout.addWidget(self.radio_aleatoire)
        radio_layout.addWidget(self.radio_personnalise)
        layout.addLayout(radio_layout)

        # Paquet personnalisé
        self.paquet_input = QLineEdit()
        self.paquet_input.setPlaceholderText("Ex: 5 de Trèfle, 53 de Joker Noir...")
        self.paquet_input.setVisible(False)
        layout.addWidget(self.paquet_input)

        # Message codé/décodé
        layout.addWidget(QLabel("Message codé :"))
        self.encoded_output = QTextEdit()
        self.encoded_output.setFixedHeight(100)
        layout.addWidget(self.encoded_output)

        layout.addWidget(QLabel("Message décodé :"))
        self.decoded_output = QTextEdit()
        self.decoded_output.setFixedHeight(100)
        layout.addWidget(self.decoded_output)

        # Ligne de séparation
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Boutons de traitement
        self.btn_coder = QPushButton("Coder")
        self.btn_decoder = QPushButton("Décoder")
        self.btn_actualiser = QPushButton("Actualiser le paquet")
        self.btn_copier = QPushButton("Copier le paquet")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_coder)
        button_layout.addWidget(self.btn_decoder)
        layout.addLayout(button_layout)

        layout.addWidget(self.btn_actualiser)
        layout.addWidget(self.btn_copier)

        # Ajouter un QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Créer un widget central pour la scroll area
        central_widget = QWidget()
        central_widget.setLayout(layout)
        scroll_area.setWidget(central_widget)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        # Connexions
        self.radio_personnalise.toggled.connect(lambda: self.paquet_input.setVisible(self.radio_personnalise.isChecked()))
        self.btn_actualiser.clicked.connect(self.actualiser_paquet)
        self.btn_coder.clicked.connect(self.coder_message)
        self.btn_decoder.clicked.connect(self.decoder_message)
        self.btn_copier.clicked.connect(self.copier_paquet)


    def get_paquet_type(self):
        if self.radio_classique.isChecked():
            return "classique"
        elif self.radio_aleatoire.isChecked():
            return "aleatoire"
        else:
            return "personnalise"

    def actualiser_paquet(self):
        try:
            paquet_type = self.get_paquet_type()
            if paquet_type == "personnalise":
                paquet_str = self.paquet_input.text()
                if not paquet_str:
                    QMessageBox.warning(self, "Erreur", "Veuillez entrer un paquet personnalisé.")
                    return
                paquet_list = JeuDeCartes.parser_depuis_chaine(paquet_str)
                jeu = JeuDeCartes(option="personnalise", paquet_personnalise=paquet_list)
            else:
                jeu = JeuDeCartes(option=paquet_type)

            self.paquet_copie = jeu.copier_paquet()
            valid, msg = jeu.valider_paquet()
            if not valid:
                QMessageBox.critical(self, "Erreur", f"Paquet invalide : {msg}")
                return
            QMessageBox.information(self, "Succès", "Paquet actualisé !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def load_txt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier texte", "", "Fichiers texte (*.txt)")
        if file_path:
            self.input_file_path = file_path
            QMessageBox.information(self, "Fichier chargé", f"Fichier sélectionné : {file_path}")
        else:
            self.input_file_path = None

    def load_crypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier crypté", "", "Fichiers cryptés (*.crypt)")
        if file_path:
            self.input_file_path = file_path
            QMessageBox.information(self, "Fichier chargé", f"Fichier sélectionné : {file_path}")
        else:
            self.input_file_path = None

    def encrypt_file(self):
        if not hasattr(self, "input_file_path") or not self.input_file_path:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord sélectionner un fichier .txt")
            return

        try:
            with open(self.input_file_path, "r", encoding="utf-8") as f:
                texte = f.read()

            paquet_type = self.get_paquet_type()
            if paquet_type == "personnalise":
                paquet_str = self.paquet_input.text()
                if not paquet_str:
                    QMessageBox.warning(self, "Erreur", "Veuillez entrer un paquet personnalisé.")
                    return
                paquet_list = JeuDeCartes.parser_depuis_chaine(paquet_str)
                jeu = JeuDeCartes(option="personnalise", paquet_personnalise=paquet_list)
            else:
                jeu = JeuDeCartes(option=paquet_type)

            # Sauvegarde du paquet initial avant toute modification
            paquet_copie = jeu.copier_paquet()
            texte_crypte = coder(texte, jeu)

            # Sauvegarde du fichier crypté
            crypted_path = self.input_file_path.replace(".txt", ".crypt")
            with open(crypted_path, "w", encoding="utf-8") as f:
                f.write(texte_crypte)

            # Sauvegarde du paquet dans un fichier .paquet pour une utilisation future
            paquet_path = self.input_file_path.replace(".txt", ".paquet")
            paquet_str = ", ".join(str(carte) for carte in paquet_copie.cartes)
            with open(paquet_path, "w", encoding="utf-8") as f:
                f.write(paquet_str)

            QMessageBox.information(self, "Succès", f"Fichier crypté :\n{crypted_path}\n\nPaquet :\n{paquet_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")


    def decrypt_file(self):
        if not hasattr(self, "input_file_path") or not self.input_file_path:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord sélectionner un fichier .crypt")
            return

        if not hasattr(self, "paquet_file_path") or not self.paquet_file_path:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner le fichier .paquet associé")
            return

        try:
            # Chargement du fichier crypté
            with open(self.input_file_path, "r", encoding="utf-8") as f:
                texte_crypte = f.read()

            # Chargement du fichier paquet
            with open(self.paquet_file_path, "r", encoding="utf-8") as f:
                paquet_str = f.read()
                paquet_list = JeuDeCartes.parser_depuis_chaine(paquet_str)
                jeu = JeuDeCartes(option="personnalise", paquet_personnalise=paquet_list)

            # Décryptage
            texte_decrypte = decoder(texte_crypte, jeu)

            # Sauvegarde du fichier décrypté
            decrypted_path = self.input_file_path.replace(".crypt", "_decrypte.txt")
            with open(decrypted_path, "w", encoding="utf-8") as f:
                f.write(texte_decrypte)

            QMessageBox.information(self, "Succès", f"Fichier déchiffré :\n{decrypted_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")


    def select_paquet_file(self):
        paquet_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier .paquet", "", "Fichiers Paquet (*.paquet)")
        if paquet_path:
            self.paquet_file_path = paquet_path
            self.paquet_label.setText(paquet_path)

    def coder_message(self):
        try:
            message = self.message_input.text()
            if not message:
                QMessageBox.warning(self, "Erreur", "Veuillez entrer un message.")
                return

            paquet_type = self.get_paquet_type()
            if paquet_type == "personnalise":
                paquet_str = self.paquet_input.text()
                if not paquet_str:
                    QMessageBox.warning(self, "Erreur", "Veuillez entrer un paquet personnalisé.")
                    return
                paquet_list = JeuDeCartes.parser_depuis_chaine(paquet_str)
                jeu = JeuDeCartes(option="personnalise", paquet_personnalise=paquet_list)
            else:
                jeu = JeuDeCartes(option=paquet_type)

            self.paquet_copie = jeu.copier_paquet()
            result = coder(message, jeu)
            self.encoded_output.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def decoder_message(self):
        try:
            if not self.paquet_copie:
                QMessageBox.critical(self, "Erreur", "Aucun paquet mémorisé pour décoder.")
                return
            message_code = self.encoded_output.toPlainText()
            jeu = self.paquet_copie.copier_paquet()
            result = decoder(message_code, jeu)
            self.decoded_output.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def copier_paquet(self):
        if not self.paquet_copie:
            QMessageBox.warning(self, "Erreur", "Aucun paquet à copier.")
            return
        paquet_str = ", ".join(str(carte) for carte in self.paquet_copie.cartes)
        pyperclip.copy(paquet_str)
        QMessageBox.information(self, "Copié", "Paquet copié dans le presse-papiers.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(850, 650)

    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()
    x = (screen_geometry.width() - win.width()) // 2
    y = (screen_geometry.height() - win.height()) // 2
    win.move(x, y)

    win.show()
    sys.exit(app.exec())
