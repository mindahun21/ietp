import 'package:flutter/material.dart';
import 'package:ietp_new/features/patient/data/api_service.dart';
import 'package:intl/intl.dart'; // Add intl package

class CheckupHistoryPage extends StatefulWidget {
  final int caseId;

  const CheckupHistoryPage({super.key, required this.caseId});

  @override
  _CheckupHistoryPageState createState() => _CheckupHistoryPageState();
}

class _CheckupHistoryPageState extends State<CheckupHistoryPage> {
  final ApiService _apiService = ApiService();
  List<Map<String, dynamic>> _checkupData = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchCheckupHistory();
  }

  Future<void> _fetchCheckupHistory() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final data = await _apiService.getCheckups(widget.caseId);
      setState(() {
        _checkupData = data.cast<Map<String, dynamic>>();
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return OrientationBuilder(
      builder: (context, orientation) {
        if (_isLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (_error != null) {
          return Center(child: Text('Error: $_error'));
        }

        return Scaffold(
          body: _checkupData.isEmpty
              ? const Center(
                  child: Text('No checkup data available.'),
                )
              : Padding(
                  padding: const EdgeInsets.all(4.0),
                  child: SingleChildScrollView(
                    scrollDirection: orientation == Orientation.portrait
                        ? Axis.horizontal
                        : Axis.vertical,
                    child: DataTable(
                      columns: const [
                        DataColumn(label: Text('Date')),
                        DataColumn(label: Text('Time')),
                        DataColumn(label: Text('BP')),
                        DataColumn(label: Text('PR')),
                        DataColumn(label: Text('RR')),
                        DataColumn(label: Text('T')),
                        DataColumn(label: Text('Input')),
                        DataColumn(label: Text('Output')),
                        DataColumn(label: Text('See More')),
                      ],
                      rows: _checkupData
                          .map((data) => DataRow(cells: [
                                DataCell(Text(data['date'] ?? 'N/A')),
                                DataCell(Text(_formatTime(data['time']))),
                                DataCell(Text(data['bp'] ?? 'N/A')),
                                DataCell(Text(data['pr'] ?? 'N/A')),
                                DataCell(Text(data['rr'] ?? 'N/A')),
                                DataCell(Text(data['t'] ?? 'N/A')),
                                DataCell(Text(data['input'] ?? 'N/A')),
                                DataCell(Text(data['output'] ?? 'N/A')),
                                DataCell(
                                  TextButton(
                                    onPressed: () {
                                      _showDetailsPopup(
                                          context, data['additional_information']);
                                    },
                                    child: const Text(
                                      'See More',
                                      style: TextStyle(fontSize: 10),
                                    ),
                                  ),
                                ),
                              ]))
                          .toList(),
                    ),
                  ),
                ),
        );
      },
    );
  }

  /// Format the time string to show only hours and minutes
  String _formatTime(String? time) {
    if (time == null) return 'N/A';
    try {
      final parsedTime = DateFormat('HH:mm:ss').parse(time);
      return DateFormat('HH:mm').format(parsedTime);
    } catch (e) {
      return time; // Return original time if parsing fails
    }
  }

  void _showDetailsPopup(BuildContext context, String? additionalInfo) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Additional Information'),
        content: Text(
          additionalInfo ?? 'No additional information provided.',
          style: const TextStyle(fontSize: 16.0),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}
