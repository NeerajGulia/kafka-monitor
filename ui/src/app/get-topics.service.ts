import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GetTopicsService {

  constructor(private http: HttpClient) { }

  getTopics(): Observable<any>{
    return this.http.get('http://13.234.16.29:10001/api/topics')
  }
}
