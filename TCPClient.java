import java.io.*;
import java.net.*;

public class TCPClient {
    public static void main(String[] args) {
        String serverAddress = "localhost";  // 替换为服务器的IP地址
        int port = 8001;

        try (Socket socket = new Socket(serverAddress, port);
             BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            String qrCode;
            while (true) {
                // 输入二维码数字编码
                System.out.print("Veuillez entrer le code QR: ");  // 输出法语提示
                qrCode = input.readLine();
                out.println(qrCode);

                if (qrCode.equalsIgnoreCase("exit")) {
                    System.out.println("Fermeture de la connexion...");  // 输出法语提示
                    break;
                }

                // 接收服务器的电影信息
                String response = in.readLine();
                if (response == null || response.equalsIgnoreCase("exit")) {
                    System.out.println("Le serveur a déconnecté");  // 输出法语提示
                    break;
                }
                System.out.println("Serveur: " + response);  // 输出法语提示
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}