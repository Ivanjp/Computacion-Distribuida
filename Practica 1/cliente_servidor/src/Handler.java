/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author beatl
 */
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.OutputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.SQLException;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.HashMap;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import io.fusionauth.jwt.JWTExpiredException;
import io.fusionauth.jwt.Signer;
import io.fusionauth.jwt.Verifier;
import io.fusionauth.jwt.domain.JWT;
import io.fusionauth.jwt.hmac.HMACSigner;
import io.fusionauth.jwt.hmac.HMACVerifier;
import java.math.BigDecimal;
import java.util.ArrayList;

public class Handler implements HttpHandler {

    String a = "";

    @Override
    public void handle(HttpExchange t) {
        try {
            Map<String, String> params = queryToMap(t.getRequestURI().getQuery());
            String tipo = params.get("op");
            int codigo = 200;
            if (tipo == null) {
                tipo = "na";
            }
            String respuesta = null;
            //se identifica el tipo de operacion y se arma la respuesta
            switch (tipo) {
                case "aut":
                    String usuario = params.get("usuario");
                    String clave = params.get("clave");
                    if (usuario == null || clave == null) {
                        codigo = 404;
                        respuesta = "Faltan parametros";
                    } else if (validaUsuario(usuario, clave)) {
                        respuesta = obtenToken(usuario);
                    } else {
                        codigo = 401;
                        respuesta = "Usuario o clave no validos";
                    }
                    //verificar que el usuario y clave sean correctos
                    break;
                case "reg":
                    String new_user = params.get("usuario");
                    String new_clave = params.get("clave");
                    String resid = params.get("resid");
                    String sexo = params.get("sexo");
                    String edad = params.get("edad");
                    int e = Integer.parseInt(edad);

                    if (new_user == null || new_clave == null || edad == null || resid == null || sexo == null) {
                        codigo = 404;
                        respuesta = "Faltan parametros";
                    } else if (agregaUsuario(new_user, new_clave, resid, sexo, e)) {
                        respuesta = "Registro exitoso.";
                    }else{
                        codigo = 412;
                        respuesta = " ";
                    }
                    break;
                case "regA":
                    String distancia = params.get("distancia");
                    String hora = params.get("hora");
                    String minu = params.get("min");
                    String seg = params.get("seg");
                    String tipo_carr = params.get("tipo");
                    String fecha = params.get("fecha");
                    String user = params.get("usuario");
                    BigDecimal dist = new BigDecimal(distancia);
                    String date = hora + ":" + minu + ":" + seg;

                    String token_a = t.getRequestHeaders().getFirst("Authorization");

                    if (token_a == null || distancia == null || hora == null || minu == null || seg == null || tipo_carr == null || fecha == null) {
                        codigo = 400;
                        respuesta = "Bad Request";
                        break;
                    }
                    String token = token_a.split(" ")[1];
                    if (!verificaToken(token)) {
                        respuesta = "No autorizado";
                        codigo = 401;
                    } else if (agregaRegistroUser(dist, date, tipo_carr, fecha, user)) {
                        respuesta = "Registro exitoso.";
                    }
                    break;
                case "BU":
                    String name = params.get("usuario");

                    String token_b = t.getRequestHeaders().getFirst("Authorization");

                    if (token_b == null || name == null) {
                        codigo = 400;
                        respuesta = "Bad Request";
                        break;
                    }

                    String token_1 = token_b.split(" ")[1];

                    if (!verificaToken(token_1)) {
                        respuesta = "No autorizado";
                        codigo = 401;
                    } else if (busquedaRU(name)) {
                        respuesta = busquedaRUResp(name);
                    }else{
                        codigo = 412;
                        respuesta = " ";
                    }
                    break;
                case "BG":
                    String tcarr = params.get("tipo");

                    String token_c = t.getRequestHeaders().getFirst("Authorization");

                    if (token_c == null || tcarr == null) {
                        codigo = 400;
                        respuesta = "Datos incompletos";
                        break;
                    }

                    String token_2 = token_c.split(" ")[1];

                    if (!verificaToken(token_2)) {
                        respuesta = "No autorizado";
                        codigo = 401;
                    } else if (busquedaG(tcarr)) {
                        respuesta = busquedaGResp(tcarr);
                    }else{
                        codigo = 412;
                        respuesta = " ";
                    }
                    break;
                default:
                    codigo = 404;
                    respuesta = "Operacion invalida";
            }
            byte[] bs = respuesta.getBytes("UTF-8");
            t.sendResponseHeaders(codigo, bs.length);
            OutputStream os = t.getResponseBody();
            os.write(bs);
            os.close();
        } catch (IOException e) {
            System.out.println(e);
        } catch (Exception k) {
            System.out.println(k);
        }
    }

    public Map<String, String> queryToMap(String query) {
        if (query == null) {
            return null;
        }
        if (query.length() == 0) {
            return null;
        }
        Map<String, String> result = new HashMap<>();
        for (String param : query.split("&")) {
            String[] entry = param.split("=");
            if (entry.length > 1) {
                result.put(entry[0], entry[1]);
            } else {
                result.put(entry[0], "");
            }
        }
        return result;
    }

    private String obtenToken(String usuario) {
        Signer signer = HMACSigner.newSHA256Signer("secreto");
        JWT jwt = new JWT().setIssuer("localhost")
                .setIssuedAt(ZonedDateTime.now(ZoneOffset.UTC))
                .setSubject(usuario)
                .setExpiration(ZonedDateTime.now(ZoneOffset.UTC).plusMinutes(1));
        String encodedJWT = JWT.getEncoder().encode(jwt, signer);
        return encodedJWT;
    }

    private boolean verificaToken(String token) {
        try {
            Verifier verifier = HMACVerifier.newVerifier("secreto");
            JWT jwt2 = JWT.getDecoder().decode(token, verifier);
        } catch (JWTExpiredException e) {
            return false;
        }
        return true;
    }

    private boolean validaUsuario(String usuario, String clave) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT * FROM Usuario where username = '" + usuario + "' and password = '" + clave + "'");
            if (resultSet.next()) {
                return true;
            }
            return false;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());
            return false;
        }

    }

    private boolean agregaUsuario(String username, String psw, String residencia, String sexo, int edad) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();
            int count = statement.executeUpdate("INSERT INTO Usuario (username,password,residencia,sexo,edad) values ('" + username + "','" + psw + "','" + residencia + "','" + sexo + "'," + edad + ");");
            if (count == 1) {
                return true;
            }
            return false;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());
            return false;
        }
    }

    private boolean agregaRegistroUser(BigDecimal dist, String tiempo, String tipo_c, String fecha, String nombre) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";
        int id = 0;

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT id FROM Usuario WHERE username = '" + nombre + "';");
            while (resultSet.next()) {

                id = resultSet.getInt("id");

            }
            int count = statement.executeUpdate("INSERT INTO Registros (id_user,distancia,tiempo,tipo_carrera,fecha) values ('" + id + "','" + dist + "','" + tiempo + "','" + tipo_c + "','" + fecha + "');");
            if (count == 1) {
                return true;
            }
            return false;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());
            return false;
        }
    }

    private boolean busquedaRU(String nombre) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";
        int id = 0;

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT id FROM Usuario WHERE username = '" + nombre + "';");
            while (resultSet.next()) {

                id = resultSet.getInt("id");

            }

            ResultSet resultSet_2 = statement.executeQuery("SELECT distancia,tiempo,tipo_carrera,fecha FROM Registros WHERE id_user = " + id + " ORDER BY distancia ASC, tiempo ASC;");

            if (resultSet_2.next()) {
                return true;
            }
            return false;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());
            return false;
        }
    }

    private String busquedaRUResp(String nombre) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";
        int id = 0;
        String str = " ";

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();
            ResultSet resultSet = statement.executeQuery("SELECT id FROM Usuario WHERE username = '" + nombre + "';");
            while (resultSet.next()) {

                id = resultSet.getInt("id");

            }

            ResultSet resultSet_2 = statement.executeQuery("SELECT distancia,tiempo,tipo_carrera,fecha FROM Registros WHERE id_user = " + id + " ORDER BY distancia ASC, tiempo ASC;");

            ArrayList<String> al = new ArrayList<String>();
            ArrayList<String> a2 = new ArrayList<String>();
            ArrayList<String> a3 = new ArrayList<String>();
            ArrayList<String> a4 = new ArrayList<String>();
            ArrayList<String> acompleto = new ArrayList<String>();

            while (resultSet_2.next()) {

                BigDecimal aw = resultSet_2.getBigDecimal("distancia");
                String a = resultSet_2.getString("tiempo");
                String t = resultSet_2.getString("tipo_carrera");
                String f = resultSet_2.getString("fecha");

                al.add(aw.toString() + ",");
                a2.add(a + ",");
                a3.add(t + ",");
                a4.add(f + ",");

            }

            acompleto.addAll(al);
            acompleto.add("|,");
            acompleto.addAll(a2);
            acompleto.add("||,");
            acompleto.addAll(a3);
            acompleto.add("|||,");
            acompleto.addAll(a4);
            acompleto.add("@");

            StringBuffer sb = new StringBuffer();

            for (String s : acompleto) {
                sb.append(s);
                sb.append(" ");
            }
            str = sb.toString();

        } catch (SQLException e) {
            System.out.println(e.getMessage());

        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());

        }
        return str;
    }
    
    private boolean busquedaG(String carrera) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();

            ResultSet resultSet = statement.executeQuery("SELECT U.username,distancia,tiempo,tipo_carrera,fecha FROM Registros AS R, Usuario AS U WHERE R.id_user = U.id AND R.tipo_carrera = '"+carrera+"' ORDER BY distancia ASC, tiempo ASC;");

            if (resultSet.next()) {
                return true;
            }
            return false;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());
            return false;
        }
    }
    
    private String busquedaGResp(String carrera) {

        String url = "jdbc:postgresql://db/postgres";
        String user = "postgres";
        String password = "1234";
        String str = " ";

        try {
            Class.forName("org.postgresql.Driver");
            Connection conn = null;
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
            Statement statement = conn.createStatement();
            
            ResultSet resultSet = statement.executeQuery("SELECT U.username,distancia,tiempo,tipo_carrera,fecha FROM Registros AS R, Usuario AS U WHERE R.id_user = U.id AND R.tipo_carrera = '"+carrera+"' ORDER BY distancia ASC, tiempo ASC;");

            ArrayList<String> nombres = new ArrayList<String>();
            ArrayList<String> dist = new ArrayList<String>();
            ArrayList<String> tiemp = new ArrayList<String>();
            ArrayList<String> tip = new ArrayList<String>();
            ArrayList<String> fecha = new ArrayList<String>();
            ArrayList<String> union = new ArrayList<String>();

            while (resultSet.next()) {

                String username = resultSet.getString("username");
                BigDecimal aw = resultSet.getBigDecimal("distancia");
                String a = resultSet.getString("tiempo");
                String t = resultSet.getString("tipo_carrera");
                String f = resultSet.getString("fecha");

                nombres.add(username + ",");
                dist.add(aw.toString() + ",");
                tiemp.add(a + ",");
                tip.add(t + ",");
                fecha.add(f + ",");

            }

            union.addAll(nombres);
            union.add("|,");
            union.addAll(dist);
            union.add("||,");
            union.addAll(tiemp);
            union.add("|||,");
            union.addAll(tip);
            union.add("||||,");
            union.addAll(fecha);
            union.add("@");

            StringBuffer sb = new StringBuffer();

            for (String s : union) {
                sb.append(s);
                sb.append(" ");
            }
            str = sb.toString();

        } catch (SQLException e) {
            System.out.println(e.getMessage());

        } catch (ClassNotFoundException f) {
            System.out.println(f.getMessage());

        }
        return str;
    }
}
