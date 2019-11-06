import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class GUI {
    private  JTextField searchTextField; //Text read to user, DO NOT EDIT
    private  JTextField textField2; //User Input
    private  JButton searchButton;
    private  JTextArea textArea1;

    public GUI() throws IOException {
        searchButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent actionEvent) {
                BufferedReader br = null;
                try {
                    br = new BufferedReader(new FileReader("NOV_Avail_Dates.txt"));
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                String x = textField2.getText();
                String line = null;
                do{
                    try {
                        line = br.readLine();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    if(x.equals(line)) textArea1.setText("TRUE");
                }while((line != null));
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void initialize(){
        textArea1.setVisible(true);
        textField2.setVisible(true);
        searchTextField.setVisible(true);
        searchButton.setVisible(true);

    }

    public static void main(String[] args) throws IOException {
        GUI gui = new GUI();
        gui.initialize();
    }
}
