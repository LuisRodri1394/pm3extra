import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true, 
  imports: [CommonModule, HttpClientModule], 
  template: `
    <h1>Meu App Teste 4</h1>
    <div *ngIf="data">
      <pre>{{ data | json }} </pre>
    </div>
    <div *ngIf="error">{{ error }}</div>
  `
})
export class AppComponent implements OnInit {
  data: any;
  error: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get('api/data').subscribe(
      (response) => this.data = response,
      (error) => this.error = error.message
    );
  }
}
