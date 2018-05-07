import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class GlobalUpdateService {

  private _updateSource = new BehaviorSubject<string>('');

  update = this._updateSource.asObservable();

  doUpdate(criteria) {
    this._updateSource.next(criteria);
  }

  constructor() { }

}
