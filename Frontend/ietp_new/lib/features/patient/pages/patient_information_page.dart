import 'package:flutter/material.dart';
import 'package:ietp_new/features/patient/data/api_service.dart';
import 'package:ietp_new/features/patient/pages/bed_position_tab.dart';
import 'package:ietp_new/features/patient/pages/checkup_page.dart';

class PatientInformationPage extends StatelessWidget {
  final int patientId; // Patient ID to fetch details

  const PatientInformationPage({super.key, required this.patientId});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text(
            'Patient',
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
          actions: [
            FutureBuilder<Map<String, dynamic>>(
              future: ApiService().getActiveCase(patientId), // Fetch the data
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return Container(
                    margin: EdgeInsets.symmetric(horizontal: 15),
                    child: const Center(
                      child: SizedBox(
                        width: 10, // Set the desired width
                        height: 10, // Set the desired height
                        child: CircularProgressIndicator(),
                      ),
                    ),
                  ); // Show a loading spinner
                } else if (snapshot.hasError || !snapshot.hasData) {
                  return Container(); // Handle error or no data state
                }

                final caseData = snapshot.data!['case'];
                final caseId = caseData['id']; // Extract caseId

                return GestureDetector(
                  onTap: () {
                    if (caseId != null) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => CheckupTabPage(caseId: caseId),
                        ),
                      );
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Case ID not available.')),
                      );
                    }
                  },
                  child: Row(
                    children: const [
                      Icon(Icons.edit_note),
                      SizedBox(width: 8),
                    ],
                  ),
                );
              },
            ),
          ],
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Details'),
              Tab(text: 'Bed Position'),
              // Tab(text: 'History'),
            ],
          ),
        ),
        body: FutureBuilder<Map<String, dynamic>>(
          future: ApiService().getActiveCase(patientId), // Call the API here
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            } else if (snapshot.hasError) {
              return Center(child: Text('Error: ${snapshot.error}'));
            } else if (!snapshot.hasData) {
              return const Center(child: Text('No data available.'));
            }

            final patient = snapshot.data!['patient'];
            final caseData = snapshot.data!['case'];

            return TabBarView(
              children: [
                // Details Tab
                _DetailsTab(
                  patientDetails: patient,
                  caseDetails: caseData,
                ),
                // Bed Position Tab
                BedPositioningPage(patientId: patientId,),
                // History Tab
                const Center(child: Text("History Info")),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _DetailsTab extends StatelessWidget {
  final Map<String, dynamic> patientDetails;
  final Map<String, dynamic> caseDetails;

  const _DetailsTab({
    required this.patientDetails,
    required this.caseDetails,
  });

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: [
        // Display patient basic details
        const Text(
          'Patient Information',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        const SizedBox(height: 8.0),
        _DetailRow(title: 'Name', value: patientDetails['full_name']),
        _DetailRow(title: 'Age', value: patientDetails['age'].toString()),
        _DetailRow(title: 'Gender', value: patientDetails['gender']),
        _DetailRow(title: 'Address', value: patientDetails['address']),
        _DetailRow(title: 'Phone', value: patientDetails['phone_number']),
        const Divider(height: 32.0),

        // Display case details
        const Text(
          'Case Information',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        const SizedBox(height: 8.0),
        _DetailRow(title: 'Status', value: caseDetails['status']),
        _DetailRow(
          title: 'Initial Diagnosis',
          value: caseDetails['initial_diagnosis']?['symptoms'] ?? 'N/A',
        ),
        _DetailRow(
          title: 'Medications',
          value: caseDetails['treatment_plan']?['medications'] ?? 'N/A',
        ),
        _DetailRow(
          title: 'Follow-Up',
          value: caseDetails['treatment_plan']?['follow_up'] ?? 'N/A',
        ),
        const Divider(height: 32.0),

        // Display treatments
        const Text(
          'Treatments',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        const SizedBox(height: 8.0),
        ..._buildTreatmentsList(caseDetails['treatments'] ?? []),
      ],
    );
  }

  List<Widget> _buildTreatmentsList(List<dynamic> treatments) {
    if (treatments.isEmpty) {
      return [
        const Text('No treatments available.', style: TextStyle(fontSize: 14))
      ];
    }

    return treatments.map<Widget>((treatment) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 4.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Treatment Name: ${treatment['treatment_name'] ?? 'N/A'}',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
            ),
            Text(
              'Treatment Type: ${treatment['treatment_type'] ?? 'N/A'}',
              style: const TextStyle(fontSize: 14),
            ),
            Text(
              'Description: ${treatment['description']['details'] ?? 'N/A'}',
              style: const TextStyle(fontSize: 14),
            ),
            const SizedBox(height: 8.0),
          ],
        ),
      );
    }).toList();
  }
}

class _DetailRow extends StatelessWidget {
  final String title;
  final String value;

  const _DetailRow({required this.title, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '$title: ',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }
}
