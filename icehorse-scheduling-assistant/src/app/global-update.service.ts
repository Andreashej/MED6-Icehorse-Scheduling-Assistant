import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class GlobalUpdateService {

  private _updateSource = new BehaviorSubject<string>('');
  private _unassignedUpdate = new BehaviorSubject<boolean>(false);
  private _testcardUpdate = new BehaviorSubject(undefined);
  private _dayUpdate = new BehaviorSubject(undefined);

  update = this._updateSource.asObservable();
  unassignedUpdate = this._unassignedUpdate.asObservable();
  testcardUpdate = this._testcardUpdate.asObservable();
  dayUpdate = this._dayUpdate.asObservable();

  doUpdate(criteria) {
    this._updateSource.next(criteria);
  }

  updateUnassigned() {
    this._unassignedUpdate.next(true);
  }

  updateTestCard(test) {
    this._testcardUpdate.next(test);
  }

  updateDay(day) {
    this._dayUpdate.next(day);
  }

  constructor() { }

}
