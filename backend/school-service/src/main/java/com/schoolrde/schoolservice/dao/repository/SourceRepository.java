package com.schoolrde.schoolservice.dao.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.SourceEntity;

public interface SourceRepository extends JpaRepository<SourceEntity,Integer>{
	
	Optional<SourceEntity> findById(Integer Id);
	
	List<SourceEntity> findBySchoolId(Integer schoolId);
}
