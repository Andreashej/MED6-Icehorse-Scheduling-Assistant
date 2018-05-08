import { Component, OnInit } from '@angular/core';
import { CompetitionImporterService } from '../competition-importer.service';
import { SettingsProviderService } from '../settings-provider.service';
import { FormsModule } from '@angular/forms';
import { GlobalUpdateService } from '../global-update.service';

@Component({
  selector: 'app-judge-editor',
  templateUrl: './judge-editor.component.html',
  styleUrls: ['./judge-editor.component.css']
})
export class JudgeEditorComponent implements OnInit {
  judges = [];
  settings = [];
  edit = false;

  constructor(private competitionImporter: CompetitionImporterService,
    private settingsProvider: SettingsProviderService,
    private updateService: GlobalUpdateService) { }

  ngOnInit() {
    this.settingsProvider.getSettings().subscribe(
      settings => this.settings = settings[0]
    );

    this.updateService.update.subscribe(
      () => this.getJudges(),
      () => console.log('Error on update')
    );
  }

  getJudges() {
    this.competitionImporter.getAllJudges().subscribe(
      judgelist => this.judges = judgelist,
      () => console.log('Could not retrieve judges')
    );
  }

  judgeHours(time, day) {
    try {
      day = time.times.find(x => x.date === day);
      return { 'hours': Math.floor(day.time / 60), 'minutes': day.time % 60, 'duration': day.time };
    } catch (e) {
      return { 'hours': 0, 'minutes': 0 };
    }
  }

  lengthOfDay(judge, day) {
    try {
      judge = judge.times.find(x => x.date === day);
      const start = new Date(judge.start);
      const end = new Date(judge.end);
      const duration = (end.getTime() - start.getTime()) / 60000;
      return { 'hours': Math.floor(duration / 60), 'minutes': duration % 60, 'duration': duration };
    } catch (e) {
      return { 'hours': 0, 'minutes': 0 };
    }
  }

  saveJudge(fname, lname, new_fname, new_lname, new_status) {
    this.competitionImporter.updateJudge(fname, lname, new_fname, new_lname, new_status).subscribe(
      () => this.getJudges());
  }
}
