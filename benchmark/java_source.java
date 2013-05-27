import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.regex.Pattern;

public class java_source {
    public static void main(String... args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        Pattern pattern = Pattern.compile(reader.readLine());
        pattern.matcher("warm up").matches();
        String input;
        System.out.println("java");
        while ((input = reader.readLine()) != null) {
            long start = System.nanoTime();
            pattern.matcher(input).matches();
            System.out.println(System.nanoTime() - start);
        }
    }
}

