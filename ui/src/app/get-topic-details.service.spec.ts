import { TestBed } from '@angular/core/testing';

import { GetTopicDetailsService } from './get-topic-details.service';

describe('GetTopicDetailsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: GetTopicDetailsService = TestBed.get(GetTopicDetailsService);
    expect(service).toBeTruthy();
  });
});
