import { TestBed, inject } from '@angular/core/testing';

import { CompetitionImporterService } from './competition-importer.service';

describe('CompetitionImporterService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CompetitionImporterService]
    });
  });

  it('should be created', inject([CompetitionImporterService], (service: CompetitionImporterService) => {
    expect(service).toBeTruthy();
  }));
});
