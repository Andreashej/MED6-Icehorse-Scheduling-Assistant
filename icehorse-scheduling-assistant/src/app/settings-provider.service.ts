import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class SettingsProviderService {

  constructor(private http: HttpClient) { }
  url = 'http://127.0.0.1:5000/settings';

  getSettings(): Observable<any> {
    return this.http.get(this.url);
  }

}
