import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { response } from 'express';


@Component({
  selector: 'app-root',
  template: `
    <h1>Meu App</h1>
    <div *ngIf="data">
      <pre>{{ data | json}} </pre>
    </div>
    <div *ngIf="error">{{error}}</div>
    `
})

export class AppComponent implements OnInit{
  data: any;
  error: string = '';

  constructor(private http: HttpClient){}

  ngOnInit() {
    this.http.get('api/data').subscribe(
      (response) => this.data = response,
      (error) => this.error = error.message
    );
  }
} 
    
