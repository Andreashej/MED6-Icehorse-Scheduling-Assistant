import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class CompetitionImporterService {

  constructor(private http: HttpClient) { }
  importUrl = 'http://127.0.0.1:5000/get-tests';
  reloadUrl = 'http://127.0.0.1:5000/reload-file';

  getTestData(): Observable<any> {
    return this.http.get(this.importUrl);
  }

  refreshTestData(): Observable<any> {
    return this.http.get(this.reloadUrl);
  }
}
