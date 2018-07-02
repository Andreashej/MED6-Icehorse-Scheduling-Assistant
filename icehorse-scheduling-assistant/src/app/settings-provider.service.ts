import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { CompetitionImporterService } from './competition-importer.service';

@Injectable()
export class SettingsProviderService {

  constructor(private http: HttpClient, private competitionImporter: CompetitionImporterService) { }
  url = 'http://127.0.0.1:5000/settings';

  getSettings(): Observable<any> {
    return this.http.get(this.url + '/' +  this.competitionImporter.activeCompetition);
  }

}
