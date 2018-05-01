import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class GlobalUpdateService {

  private _updateSource = new BehaviorSubject<boolean>(false);

  update = this._updateSource.asObservable();

  doUpdate(hasUpdates: boolean) {
    this._updateSource.next(hasUpdates);
  }

  constructor() { }

}
