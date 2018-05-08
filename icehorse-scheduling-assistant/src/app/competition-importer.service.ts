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

  saveTestState(test: string, phase: string, section_id: number, state: string, startBlock: string, start, end): Observable<any> {
    return this.http.get(
      this.base_url + test + '/' + phase + '/' + section_id + '/save/' + state + '/' + startBlock + '/' + start + '/' + end);
  }

  split(test: string, phase: string, section_id: number, lr: number, rr: number): Observable<any> {
    return this.http.get(this.base_url + 'split/' + test + '/' + phase + '/' + section_id + '/' + lr + '/' + rr);
  }

  join(test: string, phase: string, section1: number, section2: number): Observable<any> {
    return this.http.get(this.base_url + test + '/' + phase + '/join/' + section1 + '/' + section2);
  }

  addJudge(test: string, phase: string, fname: string, lname: string, date): Observable<any> {
    return this.http.get(
      this.base_url + 'set-judge/' + fname + '/' + lname + '/' + test + '/' + phase + '/' + date);
  }

  removeJudge(test: string, phase: string, fname: string, lname: string, date): Observable<any> {
    return this.http.get(
      this.base_url + 'unset-judge/' + fname + '/' + lname + '/' + test + '/' + phase + '/' + date);
  }

  getAllJudges(): Observable<any> {
    return this.http.get(this.base_url + 'get-judges');
  }

  getJudgesForTest(test: string, phase: string, date): Observable<any> {
    return this.http.get(this.base_url + 'get-judges/' + test + '/' + phase + '/' + date);
  }

  toggleFinal(test: string, phase: string): Observable<any> {
    return this.http.get(this.base_url + test + '/toggle-' + phase + '-final');
  }

  generateSchedule(): Observable<any> {
    return this.http.get(this.base_url + 'generate-schedule');
  }

  updateJudge(fname, lname, new_fname, new_lname, new_status): Observable<any> {
    return this.http.get(this.base_url + 'update-judge/' + fname + '/' + lname + '/' + new_fname + '/' + new_lname + '/' + new_status);
  }

}
