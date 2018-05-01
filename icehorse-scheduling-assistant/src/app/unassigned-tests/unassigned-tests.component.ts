import { Component, OnInit, Output, DoCheck, OnDestroy } from '@angular/core';
import { CompetitionImporterService } from '../competition-importer.service';
import { NgDragDropModule } from 'ng-drag-drop';
import { Subscription } from 'rxjs/Subscription';
import { GlobalUpdateService } from '../global-update.service';

@Component({
  selector: 'app-unassigned-tests',
  templateUrl: './unassigned-tests.component.html',
  styleUrls: ['./unassigned-tests.component.css']
})
export class UnassignedTestsComponent implements OnInit, DoCheck, OnDestroy {
  testdata;
  loading = false;
  saved;
  updates;
  subscription: Subscription;

  constructor(private competitionImporter: CompetitionImporterService, private updateService: GlobalUpdateService) { }

  ngOnInit() {
    if (this.getTestData()) {
    } else {
      this.reloadTestData();
    }

    this.subscription = this.updateService.update.subscribe(
      hasUpdates => this.updates = hasUpdates);
  }

  ngDoCheck() {
    if (this.updates) {
      this.getTestData();
    }
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  getTestData(): Boolean {
    this.competitionImporter.getTestData('unassigned').subscribe(
      data => this.testdata = data,
      () => console.log('Error')
    );

    if (this.testdata === undefined) {
      return true;
    }
    return false;
  }

  reloadTestData(): void {
    this.loading = true;
    this.competitionImporter.refreshTestData().subscribe(
      data => this.testdata = data,
      () => function () { console.log('Error when reloading'); this.loading = false; },
      () => this.loading = false
    );
  }

  onDrop(e: any) {
    this.testdata.push(e.dragData);
    this.saveTest(e.dragData.testcode, e.dragData.phase, e.dragData.section, 'unassigned', 0);
  }

  removeUnassigned(e: any) {
    this.testdata.splice(this.testdata.indexOf(e), 1);
  }

  saveTest(test, phase, section_id, state, startBlock): void {
    this.competitionImporter.saveTestState(test, phase, section_id, state, startBlock).subscribe(
      data => this.saved = data,
      error => console.log('Error when fetching data'),
      () => console.log('Successfully saved test state')
    );
  }

}
