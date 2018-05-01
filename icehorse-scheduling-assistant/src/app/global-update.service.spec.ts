import { TestBed, inject } from '@angular/core/testing';

import { GlobalUpdateService } from './global-update.service';

describe('GlobalUpdateService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GlobalUpdateService]
    });
  });

  it('should be created', inject([GlobalUpdateService], (service: GlobalUpdateService) => {
    expect(service).toBeTruthy();
  }));
});
