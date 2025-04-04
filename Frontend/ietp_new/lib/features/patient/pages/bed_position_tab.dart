import 'package:flutter/material.dart';
import 'package:ietp_new/features/patient/data/api_service.dart';

class BedPositioningPage extends StatefulWidget {
  final int patientId; // Pass patientId when navigating to this page

  const BedPositioningPage({super.key, required this.patientId});

  @override
  _BedPositioningPageState createState() => _BedPositioningPageState();
}

class _BedPositioningPageState extends State<BedPositioningPage> {
  int headAngle = 0;
  int footAngle = 0;
  int tiltAngle = 0;

  String bedNumber = 'Loading...'; // Default value
  String roomNumber = 'Loading...'; // Default value

  @override
  void initState() {
    super.initState();
    fetchBedDetails(); // Fetch bed details when the page is initialized
  }
Future<void> fetchBedDetails() async {
  ApiService apiService = ApiService();
  final response = await apiService.fetchBedDetails(widget.patientId);

  
  if (response != null) {
    if (response.containsKey('error')) {
      // Handle specific error case
      setState(() {
        bedNumber = 'Not Assigned';
        roomNumber = 'Not Assigned'; // Adjust as needed
      });
    } else {
      // Proceed with normal response handling
      setState(() {
        bedNumber = response['bed_number'] ?? 'Not Assigned';
        roomNumber = response['room_number'] ?? 'Not Assigned';
      });
    }
  } else {
    // Handle the case where response is null
    setState(() {
      bedNumber = 'Error fetching bed details';
      roomNumber = 'Error fetching room number';
    });
  }
}



  void _adjustAngle(String part, bool increase) {
    setState(() {
      if (part == 'head') {
        headAngle += increase ? 10 : -10;
      } else if (part == 'foot') {
        footAngle += increase ? 10 : -10;
      } else if (part == 'tilt') {
        tiltAngle += increase ? 10 : -10;
      }
    });
  }

  Widget _buildAdjustmentCard(String title, int currentAngle, String part) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '$title: $currentAngle°',
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.remove),
                  onPressed: () => _adjustAngle(part, false),
                  color: Colors.blue,
                ),
                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: () => _adjustAngle(part, true),
                  color: Colors.blue,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const Text(
                'Bed Positioning',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Bed Number: $bedNumber', // Display fetched bed number
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.normal,
                  color: Colors.grey,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Room Number: $roomNumber', // Display fetched room number
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.normal,
                  color: Colors.grey,
                ),
              ),
              const SizedBox(height: 16),
              _buildAdjustmentCard('Head Up/Down', headAngle, 'head'),
              const SizedBox(height: 16),
              _buildAdjustmentCard('Foot Up/Down', footAngle, 'foot'),
              const SizedBox(height: 16),
              _buildAdjustmentCard('Tilt Right', tiltAngle, 'tilt'),
              const SizedBox(height: 16),
              _buildAdjustmentCard('Tilt Right/Left', tiltAngle, 'tilt'),
            ],
          ),
        ),
      ),
    );
  }
}
