import 'package:flutter/material.dart';
import 'package:ietp_new/features/patient/pages/add_checkup.dart';
import 'checkup_history_page.dart'; // Import CheckupHistoryPage

class CheckupTabPage extends StatefulWidget {
  final int caseId; // Add caseId parameter

  const CheckupTabPage({super.key, required this.caseId});
  @override
  _CheckupTabPageState createState() => _CheckupTabPageState();
}

class _CheckupTabPageState extends State<CheckupTabPage> {
  final List<Map<String, String>> _checkupData = [];
 // Store added checkups

  void _addCheckup(Map<String, String> checkup) {
    setState(() {
      _checkupData.insert(0, checkup); // Insert new checkups at the top
    });
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Checkup Management'),
          bottom: const TabBar(
            tabs: [
              Tab(icon: Icon(Icons.add), text: 'Add Checkup'),
              Tab(icon: Icon(Icons.history), text: 'History'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            AddCheckupPage(
              onAddCheckup: _addCheckup, caseId: widget.caseId,// Pass callback for adding checkups
            ),
            CheckupHistoryPage(caseId: widget.caseId),
          ],
        ),
      ),
    );
  }
}
