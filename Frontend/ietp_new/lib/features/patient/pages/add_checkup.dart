import 'package:flutter/material.dart';
import 'package:ietp_new/features/patient/data/api_service.dart';

class AddCheckupPage extends StatefulWidget {
  final Function(Map<String, String>) onAddCheckup;
  final int caseId; // Add case ID

  const AddCheckupPage({super.key, required this.onAddCheckup, required this.caseId});

  @override
  AddCheckupPageState createState() => AddCheckupPageState();
}

class AddCheckupPageState extends State<AddCheckupPage> {
  final _formKey = GlobalKey<FormState>();
  final Map<String, String> _inputs = {
    'bp': '',
    'pr': '',
    'rr': '',
    't': '',
    'input': '',
    'output': '',
    'additional_information': '',
  };

  bool _isLoading = false;

  Future<void> _submitForm() async {
    if (_formKey.currentState?.validate() ?? false) {
      _formKey.currentState?.save();

      setState(() {
        _isLoading = true;
      });

      try {
        // Convert _inputs to the correct type for the API call
        final checkupData = Map<String, dynamic>.from(_inputs);

        // Call the API service
        await ApiService().addCheckup(widget.caseId, checkupData);

        // Notify parent widget and show success message
        widget.onAddCheckup(_inputs);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Checkup added successfully!')),
        );

        // Reset form after submission
        _formKey.currentState?.reset();
      } catch (e) {
        // Handle error
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to add checkup: $e')),
        );
      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ..._inputs.keys.map((key) {
                  final isAdditionalInfo = key == 'additional_information';
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 12.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          key.toUpperCase().replaceAll('_', ' '),
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                            color: Colors.black,
                          ),
                        ),
                        const SizedBox(height: 8),
                        CustomTextField(
                          hintText: 'Enter $key',
                          isMultiline: isAdditionalInfo,
                          onSaved: (value) {
                            _inputs[key] = value ?? '';
                          },
                        ),
                      ],
                    ),
                  );
                }),
                const SizedBox(height: 16.0),
                Center(
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _submitForm,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 32.0,
                        vertical: 12.0,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      backgroundColor: Colors.blue[700], // Darker blue
                    ),
                    child: _isLoading
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text(
                            'Add Checkup',
                            style: TextStyle(
                              fontSize: 16,
                              color: Colors.white, // White text color
                            ),
                          ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class CustomTextField extends StatelessWidget {
  final String hintText;
  final bool isMultiline;
  final void Function(String?) onSaved;

  const CustomTextField({
    super.key,
    required this.hintText,
    this.isMultiline = false,
    required this.onSaved,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      maxLines: isMultiline ? 4 : 1,
      decoration: InputDecoration(
        hintText: hintText,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(
            color: Colors.grey, // Gray border color
            width: 1.5,
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(
            color: Colors.grey, // Gray border color
            width: 1.5,
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(
            color: Colors.grey, // Gray border color
            width: 2.0,
          ),
        ),
        filled: true,
        fillColor: Colors.grey[200],
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter $hintText';
        }
        return null;
      },
      onSaved: onSaved,
      style: const TextStyle(fontSize: 14), // Smaller text size for input
    );
  }
}
