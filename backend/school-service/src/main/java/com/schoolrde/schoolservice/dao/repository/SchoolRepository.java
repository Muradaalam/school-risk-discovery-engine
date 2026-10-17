package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.schoolrde.schoolservice.entity.SchoolEntity;
import com.schoolrde.schoolservice.entity.SchoolWithIssueEntity;

public interface SchoolRepository extends JpaRepository<SchoolEntity,Long>{
    Optional<SchoolEntity> findBySchoolId(String schoolId);
    
    @Query("SELECT s FROM SchoolWithIssueEntity s WHERE s.id = :id")
    Optional<SchoolWithIssueEntity> findById(@Param("id") Integer id);
    
    boolean existsBySchoolId(String schoolId);
    void deleteBySchoolId(String schoolId);
}