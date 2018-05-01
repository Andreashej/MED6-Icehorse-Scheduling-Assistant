import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class CompetitionImporterService {

  constructor(private http: HttpClient) { }
  base_url = 'http://127.0.0.1:5000/';

  getTestData(state: string): Observable<any> {
    return this.http.get(this.base_url + 'get-tests/' + state);
  }

  refreshTestData(): Observable<any> {
    return this.http.get(this.base_url + 'reload-file');
  }

  getTestTime(test: string, phase: string): Observable<any> {
    return this.http.get(this.base_url + 'get-time/' + test + '/' + phase);
  }

  saveTestState(test: string, phase: string, section_id: number, state: string, startBlock: string): Observable<any> {
    // console.log(this.base_url + test + '/' + phase + '/' + section_id + '/save/' + state + '/' + startBlock);
    return this.http.get(this.base_url + test + '/' + phase + '/' + section_id + '/save/' + state + '/' + startBlock);
  }

  split(test: string, phase: string, section_id: number, lr: number, rr: number): Observable<any> {
    return this.http.get(this.base_url + 'split/' + test + '/' + phase + '/' + section_id + '/' + lr + '/' + rr);
  }

  join(test: string, phase: string, section1: number, section2: number): Observable<any> {
    return this.http.get(this.base_url + test + '/' + phase + '/join/' + section1 + '/' + section2);
  }

  addJudge(test: string, phase: string, judge: string): Observable<any> {
    return this.http.get(this.base_url + test + '/' + phase + '/judges/add/' + judge);
  }

  removeJudge(test: string, phase: string, judge: string): Observable<any> {
    return this.http.get(this.base_url + test + '/' + phase + '/judges/remove/' + judge);
  }

  toggleFinal(test: string, phase: string) {
    return this.http.get(this.base_url + test + '/toggle-' + phase + '-final');
  }
}
