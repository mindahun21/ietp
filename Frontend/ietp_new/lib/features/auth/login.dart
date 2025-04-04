import 'package:flutter/material.dart';
import 'package:ietp_new/features/patient/data/api_service.dart';
import 'package:ietp_new/features/patient/pages/patients_list_page.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_fonts/google_fonts.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false;
  String? _error;
  bool _obscureText = true; // Track password visibility

  Future<void> login() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      // Strip whitespace from username and password
      final username = _usernameController.text.trim();
      final password = _passwordController.text.trim();

      final token = await ApiService()
          .login(username, password); // Call the API service login method

      if (token != null) {
        setState(() {
          _isLoading = false;
        });

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Login Successful!')),
        );
        await setLoginState(true);

        // Navigate to the next screen
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => const PatientsPage(),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _error =
            'Login failed. Please try again.'; // User-friendly error message
        _isLoading = false;
      });
    }
  }

  Future<void> loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token =
        prefs.getString('authToken'); // Match the key used in api_service.dart
    if (token != null) {
      print('Saved Token: $token');
      // Use the token for authenticated requests
    }
  }

  @override
  void initState() {
    super.initState();
    loadToken(); // Check for a saved token when the app starts
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 200),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 220,
                  height: 50,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(10),
                    border:
                        Border.all(color: const Color(0XFF3F51F3), width: 1),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.grey,
                        offset: Offset(0.0, 1.0),
                        blurRadius: 6.0,
                      )
                    ],
                  ),
                  child: Center(
                    child: Text(
                      'Smart Hospital Bed',
                      style: GoogleFonts.caveatBrush(
                        textStyle: const TextStyle(
                          color: Color(0xFF3F51F3),
                          fontSize: 30,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 60),
              const SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.only(left: 20.0),
                child: Text(
                  'Username',
                  style: GoogleFonts.poppins(
                    textStyle: const TextStyle(
                      color: Colors.grey,
                      fontSize: 12,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 7),
              Padding(
                padding: const EdgeInsets.only(left: 20),
                child: CustomTextField(
                  controller: _usernameController,
                ),
              ),
              const SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.only(left: 20.0),
                child: Text(
                  'Password',
                  style: GoogleFonts.poppins(
                    textStyle: const TextStyle(
                      color: Colors.grey,
                      fontSize: 12,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 7),
              Padding(
                padding: const EdgeInsets.only(left: 20),
                child: CustomTextField(
                  hinttext: '*******',
                  controller: _passwordController,
                  obscureText: _obscureText,
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureText ? Icons.visibility : Icons.visibility_off,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscureText = !_obscureText; 
                      });
                    },
                  ),
                ),
              ),
              const SizedBox(height: 50),
              Center(
                child: GestureDetector(
                  onTap: () {
                    if (_usernameController.text.isEmpty ||
                        _passwordController.text.isEmpty) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Please fill all fields'),
                        ),
                      );
                    } else {
                      login();
                    }
                  },
                  child: Container(
                    margin: const EdgeInsets.only(top: 40),
                    width: 200,
                    height: 50,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10),
                      color: const Color(0xFF3F51F3),
                    ),
                    child: Center(
                      child: _isLoading
                          ? const CircularProgressIndicator(
                              color: Colors.white,
                            )
                          : Text(
                              'SIGN IN',
                              style: GoogleFonts.poppins(
                                textStyle: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              if (_error != null)
                Center(
                  child: Text(
                    _error!,
                    style: const TextStyle(
                      color: Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

class CustomTextField extends StatelessWidget {
  final TextEditingController controller;
  final String? hinttext;
  final bool obscureText;
  final Widget? suffixIcon;

  const CustomTextField({
    super.key,
    this.hinttext,
    required this.controller,
    this.obscureText = false,
    this.suffixIcon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 300,
      height: 50,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        color: const Color.fromARGB(255, 216, 214, 214),
      ),
      child: TextField(
        controller: controller,
        obscureText: obscureText,
        // textAlign: TextAlign.center, // Center the text horizontally
        decoration: InputDecoration(
          border: InputBorder.none,
          hintText: hinttext,
          contentPadding: const EdgeInsets.symmetric(vertical: 15, horizontal: 15), // Center text vertically
          hintStyle: GoogleFonts.poppins(
            textStyle: const TextStyle(
              color: Color.fromARGB(255, 139, 138, 138),
              fontSize: 15,
            ),
          ),
          suffixIcon: suffixIcon,
        ),
      ),
    );
  }
}

Future<void> setLoginState(bool isLoggedIn) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool('isLoggedIn', isLoggedIn);
}