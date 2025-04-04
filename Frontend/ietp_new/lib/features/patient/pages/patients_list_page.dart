import 'package:flutter/material.dart';
import 'package:ietp_new/features/auth/login.dart';
import 'package:ietp_new/features/patient/data/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'patient_information_page.dart'; // Import the Patient Information Page

class PatientsPage extends StatefulWidget {
  const PatientsPage({super.key});

  @override
  PatientsPageState createState() => PatientsPageState();
}

class PatientsPageState extends State<PatientsPage> {
  List<Map<String, dynamic>> patients = [];
  bool isLoading = true;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    fetchPatients(); // Fetch patient data from the API
  }

  Future<void> fetchPatients() async {
    final apiService = ApiService(); // Create an instance of ApiService
    try {
      final apiPatients =
          await apiService.fetchPatients(); // Call the instance method
      print(apiPatients);
      setState(() {
        patients = apiPatients
            .map((patient) => {
                  'id': patient['id'],
                  'name': patient['full_name'], // Corrected to match the Map structure
                  'status': patient['is_active'], // Only the status is returned
                  'bed': patient['bed'],
                })
            .toList();
        sortPatients();
        isLoading = false;
      });
    } catch (error) {
      setState(() {
        isLoading = false;
        errorMessage = 'Failed to fetch patients: $error';
      });
    }
  }

  void sortPatients() {
    patients.sort((a, b) {
      if (a['status'] == true && b['status'] == false) return -1;
      if (a['status'] == false && b['status'] == true) return 1;
      return 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Center(
          child: Text(
            'Patients',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
        ),
        actions: [
          Container(
            margin: const EdgeInsets.all(8),
            child: GestureDetector(
              onTap: () async {
                bool? confirmLogout = await showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return AlertDialog(
                      title: const Text('Logout Confirmation'),
                      content: const Text('Are you sure you want to logout?'),
                      actions: [
                        TextButton(
                          onPressed: () {
                            Navigator.of(context).pop(false); // User cancels logout
                          },
                          child: const Text('Cancel'),
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.of(context).pop(true); // User confirms logout
                          },
                          child: const Text('Yes',style: TextStyle(color: Colors.red)),
                        ),
                      ],
                    );
                  },
                );

                if (confirmLogout == true) {
                  // Navigate to the login page
                  await clearLoginState();
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const LoginPage(),
                    ),
                  );
                }
              },
              child: const Icon(Icons.logout, color: Colors.red),
            ),
          ),
        ],

      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage.isNotEmpty
              ? Center(child: Text(errorMessage))
              : buildPatientList(context),
    );
  }

  Widget buildPatientList(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(8),
      child: SingleChildScrollView(
        child: Column(
          children: [
            // Padding(
            //   padding: const EdgeInsets.all(8.0),
            //   child: TextField(
            //     cursorColor: const Color.fromARGB(255, 17, 86, 142),
            //     decoration: InputDecoration(
            //       prefixIcon: const Icon(Icons.search),
            //       hintText: 'Search',
            //       hintStyle: const TextStyle(
            //         color: Color.fromRGBO(143, 144, 152, 1),
            //       ),
            //       border: OutlineInputBorder(
            //         borderRadius: BorderRadius.circular(24.0),
            //         borderSide: BorderSide.none,
            //       ),
            //       filled: true,
            //       fillColor: Colors.blue[50],
            //     ),
            //     onChanged: (value) {
            //       // Implement search functionality here if needed
            //     },
            //   ),
            // ),
            const SizedBox(height: 8),
            ConstrainedBox(
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.8,
              ),
              child: ListView.builder(
                shrinkWrap: true,
                physics: const BouncingScrollPhysics(),
                itemCount: patients.length,
                itemBuilder: (context, index) {
                  final patient = patients[index];
                  final isActive = patient['status'] == true;

                  return GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => PatientInformationPage(
                            patientId: patient['id'],
                          ),
                        ),
                      );
                    },
                    child: ListTile(
                      leading: const CircleAvatar(
                        backgroundColor: Color.fromARGB(255, 62, 149, 248),
                        child: Icon(
                          Icons.person,
                          color: Color(0xFFE0F7FA),
                        ),
                      ),
                      title: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                patient['name'] ?? '',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Row(
                                children: [
                                  Container(
                                    width: 8.0,
                                    height: 8.0,
                                    decoration: BoxDecoration(
                                      color:
                                          isActive ? Colors.green : Colors.grey,
                                      shape: BoxShape.circle,
                                    ),
                                  ),
                                  const SizedBox(width: 4.0),
                                  Text(
                                    isActive ? 'Active' : 'Inactive',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color:
                                          isActive ? Colors.green : Colors.grey,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              // Dummy placeholder for bed information
                              Text(
                                patient['bed'] ?? 'bed not assigned',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: Colors.grey,
                                ),
                              ),
                              // Dummy placeholder for alert information
                              Container(
                                width: 48,
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 8.0,
                                  vertical: 4.0,
                                ),
                                decoration: BoxDecoration(
                                  color: Colors.grey,
                                  borderRadius: BorderRadius.circular(16.0),
                                ),
                                child: const Center(
                                  child: Text(
                                    'Alert',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 10,
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
Future<void> clearLoginState() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('isLoggedIn');
}