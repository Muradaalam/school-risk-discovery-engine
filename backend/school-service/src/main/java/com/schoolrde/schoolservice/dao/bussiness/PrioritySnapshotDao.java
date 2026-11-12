package com.schoolrde.schoolservice.dao.bussiness;

import java.util.Optional;

import com.schoolrde.schoolservice.entity.PrioritySnapshotEntity;

public interface PrioritySnapshotDao{
	PrioritySnapshotEntity savePrioritySnapshot(PrioritySnapshotEntity prioritySnapshot);

    Optional<PrioritySnapshotEntity> findPrioritySnapshotBySchoolId(Integer schoolId);

    Optional<PrioritySnapshotEntity> findPrioritySnapshotById(Integer id);

}
