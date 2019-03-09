import { TestBed } from '@angular/core/testing';

import { GetTopicsService } from './get-topics.service';

describe('GetTopicsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: GetTopicsService = TestBed.get(GetTopicsService);
    expect(service).toBeTruthy();
  });
});
