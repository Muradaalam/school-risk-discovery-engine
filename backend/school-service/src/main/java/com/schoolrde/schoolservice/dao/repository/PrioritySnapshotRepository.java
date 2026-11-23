package com.schoolrde.schoolservice.dao.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.PrioritySnapshotEntity;

public interface PrioritySnapshotRepository extends JpaRepository<PrioritySnapshotEntity,Integer>{
	
	Optional<PrioritySnapshotEntity> findById(Integer Id);
	
    List<PrioritySnapshotEntity> findBySchoolId(Integer schoolId);

}