import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  final String baseUrl = "https://milkiasyeheyis.tech/api";

  Future<String?> login(String username, String password) async {
    final url = Uri.parse("$baseUrl/login/");
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        "username": username,
        "password": password,
      }),
    );
    // print(response.statusCode);
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final token = data['token'];

      // Save the token to local storage
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('authToken', token);

      return token;
    } else {
      throw Exception('Failed to login: ${response.body}');
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('authToken');

    if (token == null) {
      throw Exception('No token found. Please login first.');
    }

    final url = Uri.parse("$baseUrl/logout/");
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
      },
    );

    if (response.statusCode == 204) {
      // Remove the token from local storage
      await prefs.remove('authToken');
    } else {
      throw Exception('Failed to logout: ${response.body}');
    }
  }

  Future<List<Map<String, dynamic>>> fetchPatients() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('authToken');

    if (token == null) {
      throw Exception('No token found. Please login first.');
    }

    final url = Uri.parse("$baseUrl/patients/");
    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
      },
    );

    if (response.statusCode == 200) {
      return List<Map<String, dynamic>>.from(jsonDecode(response.body));
    } else {
      throw Exception('Failed to fetch patient list: ${response.body}');
    }
  }

  // Method to fetch patient case details using patient ID
  // Future<Map<String, dynamic>> fetchPatientDetails(int id) async {
  //   final response = await http.get(
  //     Uri.parse('$baseUrl/patient/$id/case/'),
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Authorization': 'Token 7ebe8dd767a988b44e472488acd3881505ac6e01',
  //     },
  //   );

  //   if (response.statusCode == 200) {
  //     return json.decode(response.body); // Decode JSON response
  //   } else {
  //     throw Exception('Failed to load patient details');
  //   }
  // }

  Future<Map<String, dynamic>> getActiveCase(int patientId) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('authToken');

    if (token == null) {
      throw Exception('No token found. Please login first.');
    }

    final url = Uri.parse("$baseUrl/patient/$patientId/case/");
    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
      },
    );
    // print(response);

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch active case: ${response.body}');
    }
  }

  Future<List<dynamic>> getCheckups(int caseId) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('authToken');

    if (token == null) {
      throw Exception('No token found. Please login first.');
    }

    final url = Uri.parse("$baseUrl/case/$caseId/checkups/");
    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to fetch checkups: ${response.body}');
    }
  }

  Future<Map<String, dynamic>?> fetchBedDetails(int patientId) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('authToken');

    final url = Uri.parse('$baseUrl/api/bed/$patientId/');
    try {
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
      );
      print(response);
      print(response.statusCode);

      if (response.statusCode == 200) {
        // Check if the response body is not empty and return parsed JSON
        return response.body.isNotEmpty ? jsonDecode(response.body) : null;
      } else if (response.statusCode == 404) {
        // Handle 404 specifically (bed not assigned)
        print('Error: Bed not assigned (404)');
        return {'error': 'Bed not assigned'};
      } else {
        // Log other errors and return null
        print('Error: Received status code ${response.statusCode}');
        return null;
      }
    } catch (e) {
      // Log the error and return null
      print('Error: $e');
      return null;
    }
  }

  Future<void> addCheckup(int caseId, Map<String, dynamic> checkupData) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('authToken');

    if (token == null) {
      throw Exception('No token found. Please login first.');
    }

    final url = Uri.parse("$baseUrl/case/$caseId/add-checkup/");
    final response = await http.post(
      url,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
      },
      body: jsonEncode(checkupData),
    );

    if (response.statusCode != 201) {
      throw Exception('Failed to add checkup: ${response.body}');
    }
  }
}
