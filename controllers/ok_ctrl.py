from flask import render_template, request, jsonify, redirect, url_for

class OkCtrl:
    
    STATUS_OK = '200 OK'
    
    @staticmethod
    def added(element_type): 
        return jsonify({'message': f'{element_type} added successfully', 'status': OkCtrl.STATUS_OK}), 200
    
    @staticmethod
    def updated(element_type): 
        return jsonify({'message': f'{element_type} updated successfully', 'status': OkCtrl.STATUS_OK}), 200
    
    @staticmethod
    def deleted(element_type): 
        return jsonify({'message': f'{element_type} deleted successfully', 'status': OkCtrl.STATUS_OK}), 200