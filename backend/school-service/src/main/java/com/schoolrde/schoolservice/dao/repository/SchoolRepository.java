package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import com.schoolrde.schoolservice.entity.SchoolEntity;

public interface SchoolRepository extends JpaRepository<SchoolEntity,Long>{
    Optional<SchoolEntity> findBySchoolId(String schoolId);
    boolean existsBySchoolId(String schoolId);
    void deleteBySchoolId(String schoolId);
}